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
Test the Media Mangement configuration model.
"""

from __future__ import annotations

from buildarr_sonarr.config.media_management import SonarrMediaManagementSettingsConfig

NAMING_DEFAULTS = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
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

MEDIAMANAGEMENT_DEFAULTS = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
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


def test_defaults(sonarr_api) -> None:
    """
    Check that providing the default values results in a model object
    that is equal to one created directly.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets)
        == SonarrMediaManagementSettingsConfig()  # type: ignore[call-arg]
    )


def test_rename_episodes(sonarr_api) -> None:
    """
    Check that `rename_episodes` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_DEFAULTS, "renameEpisodes": True})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets)
        == SonarrMediaManagementSettingsConfig(rename_episodes=True)  # type: ignore[call-arg]
    )


def test_replace_illegal_characters(sonarr_api) -> None:
    """
    Check that `replace_illegal_characters` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_DEFAULTS, "replaceIllegalCharacters": False})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ) == SonarrMediaManagementSettingsConfig(  # type: ignore[call-arg]
        replace_illegal_characters=False,
    )
