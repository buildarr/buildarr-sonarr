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
Sonarr plugin metadata settings configuration.
"""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Tuple, Type

from buildarr.config import RemoteMapEntry
from typing_extensions import Self

from ..api import api_get, api_put
from ..secrets import SonarrSecrets
from .types import SonarrConfigBase


class Metadata(SonarrConfigBase):
    """
    Metadata definition base class.
    """

    enable: bool = False
    """
    When set to `True`, enables creating metadata files in the given format.
    """

    _implementation: ClassVar[str]
    _base_remote_map: ClassVar[List[RemoteMapEntry]] = [("enable", "enable", {})]
    _remote_map: ClassVar[List[RemoteMapEntry]]

    @classmethod
    def _from_remote(cls, metadata: Dict[str, Any]) -> Self:
        return cls(**cls.get_local_attrs(cls._base_remote_map + cls._remote_map, metadata))

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        api_metadata: Mapping[str, Any],
        check_unmanaged: bool = False,
    ) -> bool:
        updated, remote_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._base_remote_map + self._remote_map,
            check_unmanaged=check_unmanaged,
            set_unchanged=True,
        )
        if updated:
            updated_fields = {f["name"]: f["value"] for f in remote_attrs.pop("fields")}
            fields = [
                (
                    {**field, "value": updated_fields[field["name"]]}
                    if field["name"] in updated_fields
                    else field
                )
                for field in api_metadata["fields"]
            ]
            api_put(
                secrets,
                f"/api/v3/metadata/{api_metadata['id']}",
                {
                    **api_metadata,
                    **remote_attrs,
                    "fields": fields,
                },
            )
            return True
        return False


class KodiEmbyMetadata(Metadata):
    """
    Output metadata files in a format suitable for Kodi (XBMC) or Emby.

    ```yaml
    sonarr:
      settings:
        metadata:
          kodi_emby:
            enable: true
            series_metadata: true
            series_metadata_url: true
            episode_metadata: true
            series_images: true
            season_images: true
            episode_images: true
    ```
    """

    series_metadata: bool = False
    """
    Create `tvshow.nfo` with full series metadata.
    """

    series_metadata_url: bool = False
    """
    Add the TVDB show URL to `tvshow.nfo`. Can be combined with `series_metadata`.
    """

    episode_metadata: bool = False
    """
    Create episode-specific metadata as `<filename>.nfo`.
    """

    series_images: bool = False
    """
    Save series images to `fanart.jpg`, `poster.jpg` and `banner.jpg`.
    """

    season_images: bool = False
    """
    Save season images to `season##-poster.jpg`/`season-specials-poster.jpg`
    and `season##-banner.jpg`/`season-specials-banner.jpg`.
    """

    episode_images: bool = False
    """
    Save episode images to `<filename>-thumb.jpg`.
    """

    _implementation: ClassVar[str] = "XbmcMetadata"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("series_metadata", "seriesMetadata", {"is_field": True}),
        ("series_metadata_url", "seriesMetadataUrl", {"is_field": True}),
        ("episode_metadata", "episodeMetadata", {"is_field": True}),
        ("series_images", "seriesImages", {"is_field": True}),
        ("season_images", "seasonImages", {"is_field": True}),
        ("episode_images", "episodeImages", {"is_field": True}),
    ]


class RoksboxMetadata(Metadata):
    """
    Output metadata files in a format suitable for Roksbox.

    ```yaml
    sonarr:
      settings:
        metadata:
          roksbox:
            enable: true
            episode_metadata: true
            series_images: true
            season_images: true
            episode_images: true
    ```
    """

    episode_metadata: bool = False
    """
    Create episode-specific metadata as `Season##/<filename>.xml`.
    """

    series_images: bool = False
    """
    Save series images to `<Series Title>.jpg`.
    """

    season_images: bool = False
    """
    Save season images to `Season ##.jpg`.
    """

    episode_images: bool = False
    """
    Save episode images to `Season##/<filename>.jpg`.
    """

    _implementation: ClassVar[str] = "RoksboxMetadata"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("episode_metadata", "episodeMetadata", {"is_field": True}),
        ("series_images", "seriesImages", {"is_field": True}),
        ("season_images", "seasonImages", {"is_field": True}),
        ("episode_images", "episodeImages", {"is_field": True}),
    ]


class WdtvMetadata(Metadata):
    """
    Output metadata files in a format suitable for WDTV.

    ```yaml
    sonarr:
      settings:
        metadata:
          wdtv:
            enable: true
            episode_metadata: true
            series_images: true
            season_images: true
            episode_images: true
    ```
    """

    episode_metadata: bool = False
    """
    Create episode-specific metadata as `<filename>.nfo`.
    """

    series_images: bool = False
    """
    Save series images to `fanart.jpg`, `poster.jpg` and `banner.jpg`.
    """

    season_images: bool = False
    """
    Save as images to `season##-poster.jpg`/`season-specials-poster.jpg`
    and `season##-banner.jpg`/`season-specials-banner.jpg`.
    """

    episode_images: bool = False
    """
    Save episode images to `<filename>-thumb.jpg`.
    """

    _implementation: ClassVar[str] = "WdtvMetadata"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("episode_metadata", "episodeMetadata", {"is_field": True}),
        ("series_images", "seriesImages", {"is_field": True}),
        ("season_images", "seasonImages", {"is_field": True}),
        ("episode_images", "episodeImages", {"is_field": True}),
    ]


METADATA_TYPES: Tuple[Type[Metadata], ...] = (KodiEmbyMetadata, RoksboxMetadata, WdtvMetadata)
METADATA_TYPE_MAP: Dict[str, Type[Metadata]] = {
    metadata_type._implementation: metadata_type for metadata_type in METADATA_TYPES
}


class SonarrMetadataSettingsConfig(SonarrConfigBase):
    """
    Sonarr metadata settings.
    Implementation wise each metadata is a unique object, updated using separate requests.
    """

    kodi_emby: KodiEmbyMetadata = KodiEmbyMetadata()
    roksbox: RoksboxMetadata = RoksboxMetadata()
    wdtv: WdtvMetadata = WdtvMetadata()

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        kodi_emby_metadata: Optional[Dict[str, Any]] = None
        roksbox_metadata: Optional[Dict[str, Any]] = None
        wdtv_metadata: Optional[Dict[str, Any]] = None
        for metadata in api_get(secrets, "/api/v3/metadata"):
            if metadata["implementation"] == KodiEmbyMetadata._implementation:
                kodi_emby_metadata = metadata
            elif metadata["implementation"] == RoksboxMetadata._implementation:
                roksbox_metadata = metadata
            elif metadata["implementation"] == WdtvMetadata._implementation:
                wdtv_metadata = metadata
        if kodi_emby_metadata is None:
            raise RuntimeError(
                "Unable to find Kodi (XBMC)/Emby metadata on Sonarr, database might be corrupt",
            )
        if roksbox_metadata is None:
            raise RuntimeError(
                "Unable to find Roksbox metadata on Sonarr, database might be corrupt",
            )
        if wdtv_metadata is None:
            raise RuntimeError(
                "Unable to find WDTV metadata on Sonarr, database might be corrupt",
            )
        return cls(
            kodi_emby=KodiEmbyMetadata._from_remote(kodi_emby_metadata),
            roksbox=RoksboxMetadata._from_remote(roksbox_metadata),
            wdtv=WdtvMetadata._from_remote(wdtv_metadata),
        )

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        kodi_emby_metadata: Optional[Dict[str, Any]] = None
        roksbox_metadata: Optional[Dict[str, Any]] = None
        wdtv_metadata: Optional[Dict[str, Any]] = None
        for metadata in api_get(secrets, "/api/v3/metadata"):
            if metadata["implementation"] == KodiEmbyMetadata._implementation:
                kodi_emby_metadata = metadata
            elif metadata["implementation"] == RoksboxMetadata._implementation:
                roksbox_metadata = metadata
            elif metadata["implementation"] == WdtvMetadata._implementation:
                wdtv_metadata = metadata
        if kodi_emby_metadata is None:
            raise RuntimeError(
                "Unable to find Kodi (XBMC)/Emby metadata on Sonarr, database might be corrupt",
            )
        if roksbox_metadata is None:
            raise RuntimeError(
                "Unable to find Roksbox metadata on Sonarr, database might be corrupt",
            )
        if wdtv_metadata is None:
            raise RuntimeError(
                "Unable to find WDTV metadata on Sonarr, database might be corrupt",
            )
        return any(
            [
                self.kodi_emby._update_remote(
                    tree=f"{tree}.kodi_emby",
                    secrets=secrets,
                    remote=remote.kodi_emby,
                    api_metadata=kodi_emby_metadata,
                    check_unmanaged=check_unmanaged,
                ),
                self.roksbox._update_remote(
                    tree=f"{tree}.roksbox",
                    secrets=secrets,
                    remote=remote.roksbox,
                    api_metadata=roksbox_metadata,
                    check_unmanaged=check_unmanaged,
                ),
                self.wdtv._update_remote(
                    tree=f"{tree}.wdtv",
                    secrets=secrets,
                    remote=remote.wdtv,
                    api_metadata=wdtv_metadata,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )
