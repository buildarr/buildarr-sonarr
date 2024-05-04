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
Sonarr plugin tags settings configuration.
"""

from __future__ import annotations

from logging import getLogger
from typing import Dict, Set

from buildarr.types import NonEmptyStr
from typing_extensions import Self

from ..api import api_get, api_post
from ..secrets import SonarrSecrets
from .types import SonarrConfigBase

logger = getLogger(__name__)


class SonarrTagsSettingsConfig(SonarrConfigBase):
    """
    Tags are used to associate media files with certain resources (e.g. release profiles).

    ```yaml
    sonarr:
      settings:
        tags:
          definitions:
            - "example1"
            - "example2"
    ```

    To be able to use those tags in Buildarr, they need to be defined
    in this configuration section.
    """

    definitions: Set[NonEmptyStr] = set()
    """
    Define tags that are used within Buildarr here.

    If they are not defined here, you may get errors resulting from non-existent
    tags from either Buildarr or Sonarr.
    """

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        return cls(
            definitions=set(tag["label"] for tag in api_get(secrets, "/api/v3/tag")),
        )

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # This only does creations and updates, as Sonarr automatically cleans up unused tags.
        changed = False
        current_tags: Dict[str, int] = {
            tag["label"]: tag["id"] for tag in api_get(secrets, "/api/v3/tag")
        }
        if self.definitions:
            for i, tag in enumerate(sorted(self.definitions)):
                if tag in current_tags:
                    logger.debug("%s.definitions[%i]: %s (exists)", tree, i, repr(tag))
                else:
                    logger.info("%s.definitions[%i]: %s -> (created)", tree, i, repr(tag))
                    api_post(secrets, "/api/v3/tag", {"label": tag})
                    changed = True
        return changed
