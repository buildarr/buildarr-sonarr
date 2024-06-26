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
Sonarr plugin language profile configuration.
"""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum
from pydantic import Field, ValidationInfo, field_validator
from typing_extensions import Annotated, Self

from ...api import api_delete, api_get, api_post, api_put
from ...secrets import SonarrSecrets
from ..types import SonarrConfigBase

logger = getLogger(__name__)


class Language(BaseEnum):
    """
    These are the available languages that can be selected in a language profile.

    * Arabic
    * Bulgarian
    * Chinese
    * Czech
    * Danish
    * Dutch
    * English
    * Finnish
    * Flemish
    * French
    * German
    * Greek
    * Hebrew
    * Hindi
    * Hungarian
    * Icelandic
    * Italian
    * Japanese
    * Korean
    * Lithuanian
    * Malayalam
    * Norwegian
    * Polish
    * Portuguese
    * Russian
    * Spanish
    * Swedish
    * Turkish
    * Ukrainian
    * Vietnamese
    """

    arabic = "Arabic"
    bulgarian = "Bulgarian"
    chinese = "Chinese"
    czech = "Czech"
    danish = "Danish"
    dutch = "Dutch"
    english = "English"
    finnish = "Finnish"
    flemish = "Flemish"
    french = "French"
    german = "German"
    greek = "Greek"
    hebrew = "Hebrew"
    hindi = "Hindi"
    hungarian = "Hungarian"
    icelandic = "Icelandic"
    italian = "Italian"
    japanese = "Japanese"
    korean = "Korean"
    lithuanian = "Lithuanian"
    malayalam = "Malayalam"
    norwegian = "Norwegian"
    polish = "Polish"
    portuguese = "Portuguese"
    russian = "Russian"
    spanish = "Spanish"
    swedish = "Swedish"
    turkish = "Turkish"
    ukrainian = "Ukrainian"
    unknown = "Unknown"
    vietnamese = "Vietnamese"


class LanguageProfile(SonarrConfigBase):
    """
    A language profile is defined under the `language_profiles` block as shown below.

    ```yaml
    ...
      language_profiles:
        definitions:
          Anime: # Name of the language profile
            upgrades_allowed: true
            upgrade_until: "Japanese" # Required if upgrades are allowed
            languages: # Required
              - "Japanese"
              - "English"
    ```
    """

    upgrades_allowed: bool = False
    """
    Enable automatic upgrading if a version of a media file
    in a more preferred language becomes available.

    If disabled, languages will not be upgraded.
    """

    languages: Annotated[List[Language], Field(min_length=1)]
    """
    The languages episodes are allowed to be in.
    The order of the list determines priority (highest priority first, lowest priority last).

    Use the name of the language in English (e.g. `Japanese`, not `Nihongo` or `日本語`).

    ```yaml
    ...
      languages:
        - "Japanese"
        - "English"
    ```

    At least one language must be specified.
    """

    upgrade_until: Optional[Language] = None
    """
    The highest priority language to upgrade an episode to.
    Usually this would be set to the highest priority language in the profile.

    This attribute is required if `upgrades_allowed` is set to `True`.
    """

    @field_validator("languages")
    @classmethod
    def validate_languages(cls, value: List[Language]) -> List[Language]:
        language_set: Set[Language] = set()
        for language in value:
            if language in language_set:
                raise ValueError(f"duplicate entries of language '{language.value}' exist")
            else:
                language_set.add(language)
        return value

    @field_validator("upgrade_until")
    @classmethod
    def validate_upgrade_until(
        cls,
        value: Optional[Language],
        info: ValidationInfo,
    ) -> Optional[Language]:
        try:
            upgrades_allowed: bool = info.data["upgrades_allowed"]
            languages: Sequence[Language] = info.data["languages"]
        except KeyError:
            return value
        # If `upgrades_allowed` is `False`, set `upgrade_until` to `None`
        # to make sure Buildarr ignores whatever it is currently set to
        # on the remote instance.
        if not upgrades_allowed:
            return None
        # Subsequent checks now assume that `upgrades_allowed` is `True`,
        # this parameter is required and defined to a valid value.
        if not value:
            raise ValueError("required if 'upgrades_allowed' is True")
        for language in languages:
            if value == language:
                break
        else:
            raise ValueError("must be set to a value enabled in 'languages'")
        return value

    @classmethod
    def _get_remote_map(
        cls,
        language_ids: Mapping[Language, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("upgrades_allowed", "upgradeAllowed", {}),
            (
                "upgrade_until",
                "cutoff",
                {
                    "decoder": lambda v: Language(v["name"]),
                    "root_encoder": lambda vs: cls._upgrade_until_encoder(
                        language_ids=language_ids,
                        language=vs.upgrade_until if vs.upgrade_until else vs.languages[0],
                    ),
                },
            ),
            (
                "languages",
                "languages",
                {
                    "decoder": lambda v: list(
                        reversed([ln["language"]["name"] for ln in v if ln["allowed"]]),
                    ),
                    "encoder": lambda v: cls._languages_encoder(language_ids, v),
                },
            ),
        ]

    @classmethod
    def _upgrade_until_encoder(
        cls,
        language_ids: Mapping[Language, int],
        language: Language,
    ) -> Dict[str, Any]:
        return {"id": language_ids[language], "name": language.value}

    @classmethod
    def _languages_encoder(
        cls,
        language_ids: Mapping[Language, int],
        languages: List[Language],
    ) -> List[Dict[str, Any]]:
        return list(
            reversed(
                [
                    {
                        "language": {"id": language_ids[ln], "name": ln.value},
                        "allowed": True,
                    }
                    for ln in languages
                ]
                + [
                    {
                        "language": {"id": language_ids[ln], "name": ln.value},
                        "allowed": False,
                    }
                    for ln in (lang for lang in Language if lang not in languages)
                ],
            ),
        )

    @classmethod
    def _from_remote(
        cls,
        language_ids: Mapping[Language, int],
        remote_attrs: Mapping[str, Any],
    ) -> Self:
        return cls(
            **cls.get_local_attrs(cls._get_remote_map(language_ids), remote_attrs),
        )

    def _create_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        profile_name: str,
        language_ids: Mapping[Language, int],
    ) -> None:
        api_post(
            secrets,
            "/api/v3/languageprofile",
            {
                "name": profile_name,
                **self.get_create_remote_attrs(tree, self._get_remote_map(language_ids)),
            },
        )

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: LanguageProfile,
        profile_id: int,
        profile_name: str,
        language_ids: Mapping[Language, int],
    ) -> bool:
        changed, remote_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._get_remote_map(language_ids),
            check_unmanaged=True,
            set_unchanged=True,
        )
        if changed:
            api_put(
                secrets,
                f"/api/v3/languageprofile/{profile_id}",
                {"id": profile_id, "name": profile_name, **remote_attrs},
            )
            return True
        return False

    def _delete_remote(self, secrets: SonarrSecrets, profile_id: int) -> None:
        api_delete(secrets, f"/api/v3/languageprofile/{profile_id}")


class SonarrLanguageProfilesSettingsConfig(SonarrConfigBase):
    """
    Configuration parameters for controlling how Buildarr handles language profiles.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete language profiles not defined in Buildarr.
    """

    definitions: Dict[str, LanguageProfile] = {}
    """
    Define language profiles to configure on Sonarr here.

    If there are no language profiles defined and `delete_unmanaged` is `False`,
    Buildarr will not modify existing language profiles, but if `delete_unmanaged` is `True`,
    **Buildarr will delete all existing profiles. Be careful when using `delete_unmanaged`.**
    """

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        language_ids = {
            Language(language["language"]["name"]): language["language"]["id"]
            for language in api_get(secrets, "/api/v3/languageprofile/schema")["languages"]
        }
        return cls(
            definitions={
                profile["name"]: LanguageProfile._from_remote(language_ids, profile)
                for profile in api_get(secrets, "/api/v3/languageprofile")
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
        profile_ids: Dict[str, int] = {
            profile_json["name"]: profile_json["id"]
            for profile_json in api_get(secrets, "/api/v3/languageprofile")
        }
        language_ids = {
            Language(language["language"]["name"]): language["language"]["id"]
            for language in api_get(secrets, "/api/v3/languageprofile/schema")["languages"]
        }
        # # Only works on Sonarr V4
        # try:
        #     language_ids: Dict[Language, int] = {
        #         Language(language["name"]): language["id"]
        #         for language in api_get(secrets, "/api/v3/language")
        #     }
        # # Compatible with Sonarr V3, deprecated on Sonarr V4
        # except SonarrAPIError as err:
        #     if err.response.status_code == 404:
        #         ...
        #     else:
        #         raise
        for profile_name, profile in self.definitions.items():
            profile_tree = f"{tree}.definitions[{profile_name!r}]"
            if profile_name not in remote.definitions:
                profile._create_remote(
                    tree=profile_tree,
                    secrets=secrets,
                    profile_name=profile_name,
                    language_ids=language_ids,
                )
                changed = True
            elif profile._update_remote(
                tree=profile_tree,
                secrets=secrets,
                remote=remote.definitions[profile_name],
                profile_id=profile_ids[profile_name],
                profile_name=profile_name,
                language_ids=language_ids,
            ):
                changed = True
        return changed

    def delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        changed = False
        profile_ids: Dict[str, int] = {
            profile_json["name"]: profile_json["id"]
            for profile_json in api_get(secrets, "/api/v3/languageprofile")
        }
        for profile_name, profile in remote.definitions.items():
            if profile_name not in self.definitions:
                profile_tree = f"{tree}.definitions[{profile_name!r}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", profile_tree)
                    profile._delete_remote(
                        secrets=secrets,
                        profile_id=profile_ids[profile_name],
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", profile_tree)
        return changed
