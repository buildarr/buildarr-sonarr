# Copyright (C) 2024 Callum Dickinson
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
Metadata Settings unit test constants and utility functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict

XBMC_METADATA_DEFAULTS: Dict[str, Any] = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 0,
    "name": "Kodi (XBMC) / Emby",
    "implementationName": "Kodi (XBMC) / Emby",
    "implementation": "XbmcMetadata",
    "configContract": "XbmcMetadataSettings",
    "enable": False,
    "fields": [
        {"id": 0, "name": "seriesMetadata", "value": False},
        {"id": 1, "name": "seriesMetadataUrl", "value": False},
        {"id": 2, "name": "episodeMetadata", "value": False},
        {"id": 3, "name": "seriesImages", "value": False},
        {"id": 4, "name": "seasonImages", "value": False},
        {"id": 5, "name": "episodeImages", "value": False},
    ],
    "tags": [],
}

ROKSBOX_METADATA_DEFAULTS: Dict[str, Any] = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 1,
    "name": "Roksbox",
    "implementationName": "Roksbox",
    "implementation": "RoksboxMetadata",
    "configContract": "RoksboxMetadataSettings",
    "enable": False,
    "fields": [
        {"id": 0, "name": "episodeMetadata", "value": False},
        {"id": 1, "name": "seriesImages", "value": False},
        {"id": 2, "name": "seasonImages", "value": False},
        {"id": 3, "name": "episodeImages", "value": False},
    ],
    "tags": [],
}

WDTV_METADATA_DEFAULTS: Dict[str, Any] = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 2,
    "name": "WDTV",
    "implementationName": "WDTV",
    "implementation": "WdtvMetadata",
    "configContract": "WdtvMetadataSettings",
    "enable": False,
    "fields": [
        {"id": 0, "name": "episodeMetadata", "value": False},
        {"id": 1, "name": "seriesImages", "value": False},
        {"id": 2, "name": "seasonImages", "value": False},
        {"id": 3, "name": "episodeImages", "value": False},
    ],
    "tags": [],
}

METADATA_DEFAULTS = {
    "kodi_emby": XBMC_METADATA_DEFAULTS,
    "roksbox": ROKSBOX_METADATA_DEFAULTS,
    "wdtv": WDTV_METADATA_DEFAULTS,
}
