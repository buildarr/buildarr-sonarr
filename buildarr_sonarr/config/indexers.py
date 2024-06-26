# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


"""
Sonarr plugin indexers settings configuration.
"""

from __future__ import annotations

from logging import getLogger
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, RssUrl
from pydantic import AnyHttpUrl, Field, NonNegativeInt, PositiveInt, field_validator
from typing_extensions import Annotated, Self

from ..api import api_delete, api_get, api_post, api_put
from ..secrets import SonarrSecrets
from .types import SonarrConfigBase

logger = getLogger(__name__)


class NabCategory(BaseEnum):
    # https://github.com/Prowlarr/Prowlarr/blob/develop/src/NzbDrone.Core/Indexers/NewznabStandardCategory.cs
    TV = (5000, "TV")
    TV_WEBDL = (5010, "TV/WEB-DL")
    TV_FOREIGN = (5020, "TV/Foreign")
    TV_SD = (5030, "TV/SD")
    TV_HD = (5040, "TV/HD")
    TV_UHD = (5045, "TV/UHD")
    TV_OTHER = (5050, "TV/Other")
    TV_SPORT = (5060, "TV/Sport", "TV/Sports")
    TV_ANIME = (5070, "TV/Anime")
    TV_DOCUMENTARY = (5080, "TV/Documentary")
    TV_X265 = (5090, "TV/x265")

    @classmethod
    def decode(cls, value: int) -> Union[Self, int]:
        try:
            return cls(value)
        except ValueError:
            return value

    @classmethod
    def encode(cls, value: Union[Self, int]) -> int:
        return value if isinstance(value, int) else cast(int, value.value)


class FilelistCategory(BaseEnum):
    """
    Filelist category enumeration.
    """

    ANIME = "Anime"
    ANIMATION = "Animation"
    TV_4K = "TV 4K"
    TV_HD = "TV HD"
    TV_SD = "TV SD"
    SPORT = "Sport"


class Indexer(SonarrConfigBase):
    """
    Here is an example of an indexer being configured in the `indexers` configuration
    block in Buildarr.

    ```yaml
    ...
      indexers:
        definitions:
          Nyaa: # Indexer name
            type: "nyaa" # Type of indexer
            # Configuration common to all indexers
            enable_rss: true
            enable_automatic_search: true
            enable_interactive_search: true
            anime_standard_format_search: true
            indexer_priority: 25
            download_client: null
            tags:
              - "example"
            # Nyaa-specific configuration
            website_url: "https://example.com"
          # Define more indexers here.
    ```

    There are configuration parameters common to all indexer types,
    and parameters common to only specific types of indexers.

    The following configuration attributes can be defined on all indexer types.
    """

    enable_rss: bool = True
    """
    If enabled, use this indexer to watch for files that are wanted and missing
    or have not yet reached their cutoff.
    """

    enable_automatic_search: bool = True
    """
    If enabled, use this indexer for automatic searches, including Search on Add.
    """

    enable_interactive_search: bool = True
    """
    If enabled, use this indexer for manual interactive searches.
    """

    priority: Annotated[int, Field(ge=1, le=50, alias="indexer_priority")] = 25
    """
    Priority of this indexer to prefer one indexer over another in release tiebreaker scenarios.

    1 is highest priority and 50 is lowest priority.

    *Changed in version 0.4.1*: Renamed from `indexer_priority` to `priority`.
    The original name is still available as an alias.
    """

    download_client: Optional[NonEmptyStr] = None
    """
    The name of the download client to use for grabs from this indexer.
    """

    tags: List[NonEmptyStr] = []
    """
    Only use this indexer for series with at least one matching tag.
    Leave blank to use with all series.
    """

    _implementation: ClassVar[str]
    _implementation_name: ClassVar[str]
    _config_contract: ClassVar[str]
    _remote_map: ClassVar[List[RemoteMapEntry]]

    @classmethod
    def _get_base_remote_map(
        cls,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("enable_rss", "enableRss", {}),
            ("enable_automatic_search", "enableAutomaticSearch", {}),
            ("enable_interactive_search", "enableInteractiveSearch", {}),
            ("priority", "priority", {}),
            (
                "download_client",
                "downloadClientId",
                {
                    "decoder": lambda v: (
                        next(dc for dc, dc_id in download_client_ids.items() if dc_id == v)
                        if v
                        else None
                    ),
                    "encoder": lambda v: download_client_ids[v] if v else 0,
                },
            ),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: [tag for tag, tag_id in tag_ids.items() if tag_id in v],
                    "encoder": lambda v: [tag_ids[tag] for tag in v],
                },
            ),
        ]

    @classmethod
    def _from_remote(
        cls,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        remote_attrs: Mapping[str, Any],
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                cls._get_base_remote_map(download_client_ids, tag_ids) + cls._remote_map,
                remote_attrs,
            ),
        )

    def _create_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        indexer_name: str,
    ) -> None:
        api_post(
            secrets,
            "/api/v3/indexer",
            {
                "name": indexer_name,
                "implementation": self._implementation,
                "implementationName": self._implementation_name,
                "configContract": self._config_contract,
                **self.get_create_remote_attrs(
                    tree,
                    self._get_base_remote_map(download_client_ids, tag_ids) + self._remote_map,
                ),
            },
        )

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        indexer_id: int,
        indexer_name: str,
    ) -> bool:
        updated, remote_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._get_base_remote_map(download_client_ids, tag_ids) + self._remote_map,
            # TODO: check if check_unmanaged and/or set_unchanged are required (probably are)
        )
        if updated:
            api_put(
                secrets,
                f"/api/v3/indexer/{indexer_id}",
                {
                    "id": indexer_id,
                    "name": indexer_name,
                    "implementation": self._implementation,
                    "implementationName": self._implementation_name,
                    "configContract": self._config_contract,
                    **remote_attrs,
                },
            )
            return True
        return False

    def _delete_remote(self, secrets: SonarrSecrets, indexer_id: int) -> None:
        api_delete(secrets, f"/api/v3/indexer/{indexer_id}")


class UsenetIndexer(Indexer):
    """
    Usenet indexer base class.
    """

    pass


class TorrentIndexer(Indexer):
    """
    Configuration attributes common to all torrent indexers.
    """

    minimum_seeders: PositiveInt = 1
    """
    The minimum number of seeders required before downloading a release.
    """

    seed_ratio: Optional[float] = None
    """
    The seed ratio a torrent should reach before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    seed_time: Optional[int] = None  # minutes
    """
    The amount of time (in minutes) a torrent should be seeded before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    seasonpack_seed_time: Optional[int] = None  # minutes
    """
    The amount of time (in minutes) a season-pack torrent should be seeded before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    @classmethod
    def _get_base_remote_map(
        cls,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            *super()._get_base_remote_map(download_client_ids, tag_ids),
            ("minimum_seeders", "minimumSeeders", {"is_field": True, "field_default": None}),
            ("seed_ratio", "seedCriteria.seedRatio", {"is_field": True, "field_default": None}),
            ("seed_time", "seedCriteria.seedTime", {"is_field": True, "field_default": None}),
            (
                "seasonpack_seed_time",
                "seedCriteria.seasonPackSeedTime",
                {"is_field": True, "field_default": None},
            ),
        ]


class FanzubIndexer(UsenetIndexer):
    """
    An indexer which uses a Fanzub-compatible RSS feed to monitor for releases.
    """

    type: Literal["fanzub"] = "fanzub"
    """
    Type value associated with this kind of indexer.
    """

    rss_url: RssUrl
    """
    A URL to a Fanzub compatible RSS feed.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    _implementation = "Fanzub"
    _implementation_name = "Fanzub"
    _config_contract = "FanzubSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("rss_url", "rssUrl", {"is_field": True}),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
    ]


class NewznabIndexer(UsenetIndexer):
    """
    An indexer for monitoring a Newznab-compliant Usenet indexing site.

    Sonarr defines presets for several popular sites.
    """

    type: Literal["newznab"] = "newznab"
    """
    Type value associated with this kind of indexer.
    """

    url: AnyHttpUrl
    """
    URL of the Newznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"
    """
    Newznab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Newznab API.
    """

    categories: Set[Union[NabCategory, int]] = {NabCategory.TV_SD, NabCategory.TV_HD}
    """
    Categories to monitor for standard/daily shows.
    Define as empty to disable.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_categories: Set[NabCategory] = set()
    """
    Categories to monitor for anime.
    Define as empty to disable.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Newznab API parameters.
    """

    _implementation = "Newznab"
    _implementation_name = "Newznab"
    _config_contract = "NewznabSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]

    @field_validator("categories", "anime_categories")
    @classmethod
    def validate_categories(
        cls,
        value: Iterable[Union[NabCategory, int]],
    ) -> Set[Union[NabCategory, int]]:
        return set(
            NabCategory.decode(category) if isinstance(category, int) else category
            for category in value
        )


class OmgwtfnzbsIndexer(UsenetIndexer):
    """
    An indexer for monitoring OmgWtfNZBs.
    """

    type: Literal["omgwtfnzbs"] = "omgwtfnzbs"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    Username for the OmgWtfNZBs account.
    """

    api_key: Password
    """
    API key for the OmgWtfNZBs API.
    """

    delay: NonNegativeInt = 30  # minutes
    """
    Time (in minutes) to delay new NZBs before they appear on the RSS feed.
    """

    _implementation = "Omgwtfnzbs"
    _implementation_name = "omgwtfnzbs"
    _config_contract = "OmgwtfnzbsSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("username", "username", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("delay", "delay", {"is_field": True}),
    ]


class BroadcasthenetIndexer(TorrentIndexer):
    """
    Indexer for monitoring for new releases on BroacasTheNet.
    """

    type: Literal["broadcasthenet"] = "broadcasthenet"
    """
    Type value associated with this kind of indexer.
    """

    api_url: AnyHttpUrl = AnyHttpUrl("https://api.broadcasthe.net")
    """
    BroadcasTheNet API URL.
    """

    api_key: Password
    """
    BroadcasTheNet API key.
    """

    _implementation = "BroadcastheNet"
    _implementation_name = "BroadcasTheNet"
    _config_contract = "BroadcastheNetSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("api_url", "apiUrl", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
    ]


class FilelistIndexer(TorrentIndexer):
    """
    Monitor for new releases on FileList.io.
    """

    type: Literal["filelist"] = "filelist"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    FileList username.
    """

    passkey: Password
    """
    FileList account API key.
    """

    api_url: AnyHttpUrl = AnyHttpUrl("https://filelist.io")
    """
    FileList API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    categories: Set[FilelistCategory] = {
        FilelistCategory.TV_SD,
        FilelistCategory.TV_HD,
        FilelistCategory.TV_4K,
    }
    """
    Categories to monitor for standard/daily show new releases.

    Set to an empty list to not monitor for standard/daily shows.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    anime_categories: Set[FilelistCategory] = set()
    """
    Categories to monitor for anime new releases.

    Leave empty to not monitor for anime.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    _implementation = "FileList"
    _implementation_name = "FileList"
    _config_contract = "FilelistSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("username", "username", {"is_field": True}),
        ("passkey", "passKey", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
    ]


class HdbitsIndexer(TorrentIndexer):
    """
    Monitor for new releases on HDBits.
    """

    type: Literal["hdbits"] = "hdbits"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    HDBits account username.
    """

    api_key: Password
    """
    HDBits API key assigned to the account.
    """

    api_url: AnyHttpUrl = AnyHttpUrl("https://hdbits.org")
    """
    HDBits API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    _implementation = "HDBits"
    _implementation_name = "HDBits"
    _config_contract = "HDBitsSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("username", "username", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
    ]


class IptorrentsIndexer(TorrentIndexer):
    """
    Monitor for releases using the IP Torrents native API.

    !!! note
        IP Torrents' native API does not support automatic searching.
        It is recommended to instead configure IP Torrents as a Torznab indexer.
    """

    type: Literal["iptorrents"] = "iptorrents"
    """
    Type value associated with this kind of indexer.
    """

    # NOTE: automatic_search and interactive_search are not supported
    # by this indexer, therefore its value is ignored.

    feed_url: RssUrl
    """
    The full RSS feed url generated by IP Torrents, using only the categories
    you selected (HD, SD, x264, etc ...).
    """

    _implementation = "IPTorrents"
    _implementation_name = "IP Torrents"
    _config_contract = "IptorrentsSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("feed_url", "feedUrl", {"is_field": True}),
    ]


class NyaaIndexer(TorrentIndexer):
    """
    Monitor for new anime releases on the configured Nyaa domain.

    Nyaa only supports searching for Anime series type releases.
    """

    type: Literal["nyaa"] = "nyaa"
    """
    Type value associated with this kind of indexer.
    """

    website_url: AnyHttpUrl
    """
    HTTPS URL for accessing Nyaa.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = "&cats=1_0&filter=1"
    """
    Parameters to send in the Nyaa search request.

    Note that if you change the category, you will have to add
    required/restricted rules about the subgroups to avoid foreign language releases.
    """

    _implementation = "Nyaa"
    _implementation_name = "Nyaa"
    _config_contract = "NyaaSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("website_url", "websiteUrl", {"is_field": True}),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]


class RarbgIndexer(TorrentIndexer):
    """
    Monitor for new releases on the RARBG torrent tracker.
    """

    type: Literal["rarbg"] = "rarbg"
    """
    Type value associated with this kind of indexer.
    """

    api_url: AnyHttpUrl
    """
    RARBG API url.
    """

    ranked_only: bool = False
    """
    Only include ranked results.
    """

    captcha_token: Optional[str] = None
    """
    CAPTCHA clearance token used to handle CloudFlare anti-DDoS measures on shared-IP VPNs.
    """

    _implementation = "Rarbg"
    _implementation_name = "Rarbg"
    _config_contract = "RarbgSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("api_url", "apiUrl", {"is_field": True}),
        ("ranked_only", "rankedOnly", {"is_field": True}),
        (
            "captcha_token",
            "captchaToken",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]


class TorrentrssfeedIndexer(TorrentIndexer):
    """
    Generic parser for monitoring a torrent RSS feed.

    !!! note
        This indexer does not support automatic searching.
        It is recommended to use an indexer that natively communicates with
        a tracker using an API.
    """

    type: Literal["torrentrssfeed"] = "torrentrssfeed"
    """
    Type value associated with this kind of indexer.
    """

    # NOTE: automatic_search and interactive_search are not supported
    # by this indexer, therefore its value is ignored.

    full_rss_feed_url: RssUrl
    """
    RSS feed to monitor.
    """

    cookie: Optional[str] = None
    """
    Session cookie for accessing the RSS feed.

    If the RSS feed requires one, this should be retrieved manually via a web browser.
    """

    allow_zero_size: bool = False
    """
    Allow access to releases that don't specify release size.

    As size checks will not be performed, be careful when enabling this option.
    """

    _implementation = "TorrentRssIndexer"
    _implementation_name = "Torrent RSS Feed"
    _config_contract = "TorrentRssIndexerSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("full_rss_feed_url", "feedUrl", {"is_field": True}),
        (
            "cookie",
            "cookie",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("allow_zero_size", "allowZeroSize", {"is_field": True}),
    ]


class TorrentleechIndexer(TorrentIndexer):
    """
    Monitor for new releases on TorrentLeech.

    !!! note
        This indexer does not support automatic searching.
    """

    type: Literal["torrentleech"] = "torrentleech"
    """
    Type value associated with this kind of indexer.
    """

    # NOTE: automatic_search and interactive_search are not supported
    # by this indexer, therefore its value is ignored.

    website_url: AnyHttpUrl = AnyHttpUrl("http://rss.torrentleech.org")
    """
    TorrentLeech feed API URL.
    """

    api_key: Password
    """
    TorrentLeech API key.
    """

    _implementation = "Torrentleech"
    _implementation_name = "TorrentLeech"
    _config_contract = "TorrentleechSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("website_url", "baseUrl", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
    ]


class TorznabIndexer(TorrentIndexer):
    """
    Monitor and search for new releases on a Torznab-compliant torrent indexing site.

    Sonarr defines presets for several popular sites.
    """

    type: Literal["torznab"] = "torznab"
    """
    Type value associated with this kind of indexer.
    """

    url: AnyHttpUrl
    """
    URL of the Torznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"
    """
    Tornab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Torznab API.
    """

    categories: Set[NabCategory] = {NabCategory.TV_SD, NabCategory.TV_HD}
    """
    Categories to monitor for standard/daily shows.
    Define as empty to disable.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_categories: Set[NabCategory] = set()
    """
    Categories to monitor for anime.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Torznab API parameters.
    """

    _implementation = "Torznab"
    _implementation_name = "Torznab"
    _config_contract = "TorznabSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]

    @field_validator("categories", "anime_categories")
    @classmethod
    def validate_categories(
        cls,
        value: Iterable[Union[NabCategory, int]],
    ) -> Set[Union[NabCategory, int]]:
        return set(
            NabCategory.decode(category) if isinstance(category, int) else category
            for category in value
        )


INDEXER_TYPES: Tuple[Type[Indexer], ...] = (
    FanzubIndexer,
    NewznabIndexer,
    OmgwtfnzbsIndexer,
    BroadcasthenetIndexer,
    FilelistIndexer,
    HdbitsIndexer,
    IptorrentsIndexer,
    NyaaIndexer,
    RarbgIndexer,
    TorrentrssfeedIndexer,
    TorrentleechIndexer,
    TorznabIndexer,
)

INDEXER_TYPE_MAP: Dict[str, Type[Indexer]] = {
    indexer_type._implementation: indexer_type for indexer_type in INDEXER_TYPES
}

IndexerType = Union[
    FanzubIndexer,
    NewznabIndexer,
    OmgwtfnzbsIndexer,
    BroadcasthenetIndexer,
    FilelistIndexer,
    HdbitsIndexer,
    IptorrentsIndexer,
    NyaaIndexer,
    RarbgIndexer,
    TorrentrssfeedIndexer,
    TorrentleechIndexer,
    TorznabIndexer,
]


class SonarrIndexersSettingsConfig(SonarrConfigBase):
    """
    Indexers are used to monitor for new releases of media on external trackers.
    When a suitable release has been found, Sonarr registers it for download
    on one of the configured download clients.

    ```yaml
    sonarr:
      config:
        indexers:
          minimum_age: 0
          retention: 0
          maximum_size: 0
          rss_sync_interval: 15
          delete_unmanaged: false # Better to leave off for the most part
          definitions:
            Nyaa: # Indexer name
              type: "nyaa" # Type of indexer
              # Configuration common to all indexers
              enable_rss: true
              enable_automatic_search: true
              enable_interactive_search: true
              anime_standard_format_search: true
              indexer_priority: 25
              download_client: null
              tags:
                - "example"
              # Nyaa-specific configuration
              website_url: "https://example.com"
            # Define more indexers here.
    ```

    The following parameters are available for configuring indexers and
    how they are handled by Sonarr.

    For more information on how Sonarr finds epsiodes, refer to the FAQ on
    [WikiArr](https://wiki.servarr.com/sonarr/faq#how-does-sonarr-find-episodes).
    """

    minimum_age: NonNegativeInt = 0  # minutes
    """
    Minimum age (in minutes) of NZBs before they are grabbed. (Usenet only)

    Use this to give new releases time to propagate to your Usenet provider.
    """

    retention: NonNegativeInt = 0  # days
    """
    Retention of releases. (Usenet only)

    Set to `0` for unlimited retention.
    """

    maximum_size: NonNegativeInt = 0  # MB
    """
    Maximum size for a release to be grabbed, in megabytes (MB).

    Set to `0` to set for unlimited size.
    """

    rss_sync_interval: NonNegativeInt = 15  # minutes
    """
    Interval (in minutes) to sync RSS feeds with indexers.

    Set to `0` to disable syncing. This also disables automatic release grabbing.
    """

    # TODO: Take into account the indexers created by Prowlarr instances.
    delete_unmanaged: bool = False
    """
    Automatically delete indexers not configured by Buildarr.

    Take care when enabling this option, as it will also delete indexers
    created by external applications such as Prowlarr.

    If unsure, leave set at the default of `false`.
    """

    definitions: Dict[str, Annotated[IndexerType, Field(discriminator="type")]] = {}
    """
    Indexers to manage via Buildarr are defined here.
    """

    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("minimum_age", "minimumAge", {}),
        ("retention", "retention", {}),
        ("maximum_size", "maximumSize", {}),
        ("rss_sync_interval", "rssSyncInterval", {}),
    ]

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        indexer_config = api_get(secrets, "/api/v3/config/indexer")
        indexers = api_get(secrets, "/api/v3/indexer")
        download_client_ids: Dict[str, int] = (
            {dc["name"]: dc["id"] for dc in api_get(secrets, "/api/v3/downloadclient")}
            if any(indexer_metadata["downloadClientId"] for indexer_metadata in indexers)
            else {}
        )
        tag_ids: Dict[str, int] = (
            {tag["label"]: tag["id"] for tag in api_get(secrets, "/api/v3/tag")}
            if any(indexer["tags"] for indexer in indexers)
            else {}
        )
        return cls(
            **cls.get_local_attrs(cls._remote_map, indexer_config),
            definitions={
                indexer["name"]: INDEXER_TYPE_MAP[  # type: ignore[misc]
                    indexer["implementationName"]
                ]._from_remote(
                    download_client_ids=download_client_ids,
                    tag_ids=tag_ids,
                    remote_attrs=indexer,
                )
                for indexer in indexers
            },
        )

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        changed = False
        indexer_ids: Dict[str, int] = {
            indexer["name"]: indexer["id"] for indexer in api_get(secrets, "/api/v3/indexer")
        }
        download_client_ids: Dict[str, int] = (
            {dc["name"]: dc["id"] for dc in api_get(secrets, "/api/v3/downloadclient")}
            if any(indexer.download_client for indexer in self.definitions.values())
            or any(indexer.download_client for indexer in remote.definitions.values())
            else {}
        )
        tag_ids: Dict[str, int] = (
            {tag["label"]: tag["id"] for tag in api_get(secrets, "/api/v3/tag")}
            if any(indexer.tags for indexer in self.definitions.values())
            or any(indexer.tags for indexer in remote.definitions.values())
            else {}
        )
        config_changed, config_remote_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._remote_map,
            check_unmanaged=check_unmanaged,
        )
        if config_changed:
            api_put(
                secrets,
                f"/api/v3/config/indexer/{api_get(secrets, '/api/v3/config/indexer')['id']}",
                config_remote_attrs,
            )
            changed = True
        for indexer_name, indexer in self.definitions.items():
            indexer_tree = f"{tree}.definitions[{indexer_name!r}]"
            if indexer_name not in remote.definitions:
                indexer._create_remote(
                    tree=indexer_tree,
                    secrets=secrets,
                    download_client_ids=download_client_ids,
                    tag_ids=tag_ids,
                    indexer_name=indexer_name,
                )
                changed = True
            elif indexer._update_remote(
                tree=indexer_tree,
                secrets=secrets,
                remote=remote.definitions[indexer_name],  # type: ignore[arg-type]
                download_client_ids=download_client_ids,
                tag_ids=tag_ids,
                indexer_id=indexer_ids[indexer_name],
                indexer_name=indexer_name,
            ):
                changed = True
        return changed

    def delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        changed = False
        indexer_ids: Dict[str, int] = {
            indexer["name"]: indexer["id"] for indexer in api_get(secrets, "/api/v3/indexer")
        }
        for indexer_name, indexer in remote.definitions.items():
            if indexer_name not in self.definitions:
                indexer_tree = f"{tree}.definitions[{indexer_name!r}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", indexer_tree)
                    indexer._delete_remote(
                        secrets=secrets,
                        indexer_id=indexer_ids[indexer_name],
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", indexer_tree)
        return changed
