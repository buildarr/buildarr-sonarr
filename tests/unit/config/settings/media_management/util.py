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
Media Management unit test constants and utility functions.
"""

from __future__ import annotations

NAMING_CONFIG_DEFAULTS = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 0,
    "renameEpisodes": False,
    "replaceIllegalCharacters": True,
    "standardEpisodeFormat": (
        "{Series TitleYear} - "
        "S{season:00}E{episode:00} - "
        "{Episode CleanTitle} "
        "[{Preferred Words }{Quality Full}]"
        "{[MediaInfo VideoDynamicRangeType]}"
        "{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}"
        "{MediaInfo AudioLanguages}"
        "{[MediaInfo VideoCodec]}"
        "{-Release Group}"
    ),
    "dailyEpisodeFormat": (
        "{Series TitleYear} - "
        "{Air-Date} - "
        "{Episode CleanTitle} "
        "[{Preferred Words }{Quality Full}]"
        "{[MediaInfo VideoDynamicRangeType]}"
        "{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}"
        "{MediaInfo AudioLanguages}"
        "{[MediaInfo VideoCodec]}"
        "{-Release Group}"
    ),
    "animeEpisodeFormat": (
        "{Series TitleYear} - "
        "S{season:00}E{episode:00} - "
        "{absolute:000} - "
        "{Episode CleanTitle} "
        "[{Preferred Words }{Quality Full}]"
        "{[MediaInfo VideoDynamicRangeType]}"
        "[{MediaInfo VideoBitDepth}bit]"
        "{[MediaInfo VideoCodec]}"
        "[{Mediainfo AudioCodec} { Mediainfo AudioChannels}]"
        "{MediaInfo AudioLanguages}"
        "{-Release Group}"
    ),
    "seriesFolderFormat": "{Series TitleYear}",
    "seasonFolderFormat": "Season {season:00}",
    "specialsFolderFormat": "Specials",
    "multiEpisodeStyle": 4,  # range
}

MEDIAMANAGEMENT_CONFIG_DEFAULTS = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 0,
    # Folders
    "createEmptySeriesFolders": False,
    "deleteEmptyFolders": False,
    # Importing
    "episodeTitleRequired": "always",
    "skipFreeSpaceCheckWhenImporting": False,
    "minimumFreeSpaceWhenImporting": 100,  # MB
    "copyUsingHardlinks": True,
    "importExtraFiles": False,
    # File Management
    "autoUnmonitorPreviouslyDownloadedEpisodes": False,
    "downloadPropersAndRepacks": "doNotPrefer",
    "enableMediaInfo": True,
    "rescanAfterRefresh": "always",
    "fileDate": "none",
    "recycleBin": "",
    "recycleBinCleanupDays": 7,
    # Permissions
    "setPermissionsLinux": False,
    "chmodFolder": "755",
    "chownGroup": "",
}
