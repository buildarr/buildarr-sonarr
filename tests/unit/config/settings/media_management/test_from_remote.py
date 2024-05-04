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
Test the `from_remote` class method on the Media Management configuration model.
"""

from __future__ import annotations

import pytest

from buildarr_sonarr.config.media_management import (
    ChangeFileDate,
    ChmodFolder,
    EpisodeTitleRequired,
    MultiEpisodeStyle,
    PropersAndRepacks,
    RescanSeriesFolderAfterRefresh,
    SonarrMediaManagementSettingsConfig,
)

from .util import MEDIAMANAGEMENT_CONFIG_DEFAULTS, NAMING_CONFIG_DEFAULTS


def test_defaults(sonarr_api) -> None:
    """
    Check that providing the default values results in a model object
    that is equal to one created directly.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets)
        == SonarrMediaManagementSettingsConfig()  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_rename_episodes(sonarr_api, attr_value) -> None:
    """
    Check that the `rename_episodes` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "renameEpisodes": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).rename_episodes
        is attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_replace_illegal_characters(sonarr_api, attr_value) -> None:
    """
    Check that the `replace_illegal_characters` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "replaceIllegalCharacters": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(
            sonarr_api.secrets,
        ).replace_illegal_characters
        is attr_value
    )


def test_standard_episode_format(sonarr_api) -> None:
    """
    Check that the `standard_episode_format` attribute is being populated by its API value.
    """

    attr_value = "{Series TitleYear} - S{season:00}E{episode:00} - {Episode CleanTitle}"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "standardEpisodeFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).standard_episode_format
        == attr_value
    )


def test_daily_episode_format(sonarr_api) -> None:
    """
    Check that the `daily_episode_format` attribute is being populated by its API value.
    """

    attr_value = "{Series TitleYear} - {Air-Date} - {Episode CleanTitle}"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "dailyEpisodeFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).daily_episode_format
        == attr_value
    )


def test_anime_episode_format(sonarr_api) -> None:
    """
    Check that the `anime_episode_format` attribute is being populated by its API value.
    """

    attr_value = (
        "{Series TitleYear} - S{season:00}E{episode:00} - {absolute:000} - {Episode CleanTitle}"
    )

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "animeEpisodeFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).anime_episode_format
        == attr_value
    )


def test_series_folder_format(sonarr_api) -> None:
    """
    Check that the `series_folder_format` attribute is being populated by its API value.
    """

    attr_value = "{Series Title}"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "seriesFolderFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).series_folder_format
        == attr_value
    )


def test_season_folder_format(sonarr_api) -> None:
    """
    Check that the `season_folder_format` attribute is being populated by its API value.
    """

    attr_value = "Season {season}"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "seasonFolderFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).season_folder_format
        == attr_value
    )


def test_specials_folder_format(sonarr_api) -> None:
    """
    Check that the `specials_folder_format` attribute is being populated by its API value.
    """

    attr_value = "Special"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "specialsFolderFormat": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).specials_folder_format
        == attr_value
    )


@pytest.mark.parametrize("attr_value", list(range(6)))
def test_multiepisode_style(sonarr_api, attr_value) -> None:
    """
    Check that the `multiepisode_style` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "multiEpisodeStyle": attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).multiepisode_style == MultiEpisodeStyle(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_create_empty_series_folders(sonarr_api, attr_value) -> None:
    """
    Check that the `create_empty_series_folders` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "createEmptySeriesFolders": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(
            sonarr_api.secrets,
        ).create_empty_series_folders
        is attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_delete_empty_folders(sonarr_api, attr_value) -> None:
    """
    Check that the `delete_empty_folders` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "deleteEmptyFolders": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).delete_empty_folders
        is attr_value
    )


@pytest.mark.parametrize("attr_value", ["always", "bulkSeasonReleases", "never"])
def test_episode_title_required(sonarr_api, attr_value) -> None:
    """
    Check that the `episode_title_required` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "episodeTitleRequired": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).episode_title_required == EpisodeTitleRequired(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_skip_free_space_check(sonarr_api, attr_value) -> None:
    """
    Check that the `skip_free_space_check` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "skipFreeSpaceCheckWhenImporting": attr_value},
    )
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).skip_free_space_check
        is attr_value
    )


def test_minimum_free_space(sonarr_api) -> None:
    """
    Check that the `minimum_free_space` attribute is being populated by its API value.
    """

    attr_value = 200

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "minimumFreeSpaceWhenImporting": attr_value},
    )
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(
            sonarr_api.secrets,
        ).minimum_free_space
        == attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_use_hardlinks(sonarr_api, attr_value) -> None:
    """
    Check that the `use_hardlinks` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "copyUsingHardlinks": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).use_hardlinks
        is attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_import_extra_files(sonarr_api, attr_value) -> None:
    """
    Check that the `import_extra_files` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "importExtraFiles": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).import_extra_files
        is attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_unmonitor_deleted_episodes(sonarr_api, attr_value) -> None:
    """
    Check that the `unmonitor_deleted_episodes` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {
            **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
            "autoUnmonitorPreviouslyDownloadedEpisodes": attr_value,
        },
    )
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(
            sonarr_api.secrets,
        ).unmonitor_deleted_episodes
        is attr_value
    )


@pytest.mark.parametrize("attr_value", ["preferAndUpgrade", "doNotUpgrade", "doNotPrefer"])
def test_propers_and_repacks(sonarr_api, attr_value) -> None:
    """
    Check that the `propers_and_repacks` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "downloadPropersAndRepacks": attr_value},
    )
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).propers_and_repacks == PropersAndRepacks(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_analyze_video_files(sonarr_api, attr_value) -> None:
    """
    Check that the `analyze_video_files` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "enableMediaInfo": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).analyze_video_files
        is attr_value
    )


@pytest.mark.parametrize("attr_value", ["always", "afterManual", "never"])
def test_rescan_series_folder_after_refresh(sonarr_api, attr_value) -> None:
    """
    Check that the `rescan_series_folder_after_refresh` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "rescanAfterRefresh": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).rescan_series_folder_after_refresh == RescanSeriesFolderAfterRefresh(attr_value)


@pytest.mark.parametrize("attr_value", ["none", "localAirDate", "utcAirDate"])
def test_change_file_date(sonarr_api, attr_value) -> None:
    """
    Check that the `change_file_date` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "fileDate": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).change_file_date == ChangeFileDate(attr_value)


@pytest.mark.parametrize("attr_value", [None, "", "/opt/recycling-bin"])
def test_recycling_bin(sonarr_api, attr_value) -> None:
    """
    Check that the `recycling_bin` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "recycleBin": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).recycling_bin == (
        attr_value or None
    )


def test_recycling_bin_cleanup(sonarr_api) -> None:
    """
    Check that the `recycling_bin_cleanup` attribute is being populated by its API value.
    """

    attr_value = 30

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "recycleBinCleanupDays": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).recycling_bin_cleanup
        == attr_value
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_set_permissions(sonarr_api, attr_value) -> None:
    """
    Check that the `set_permissions` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "setPermissionsLinux": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert (
        SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).set_permissions
        is attr_value
    )


@pytest.mark.parametrize("attr_value", ["755", "775", "770", "750", "777"])
def test_chmod_folder(sonarr_api, attr_value) -> None:
    """
    Check that the `chmod_folder` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "chmodFolder": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(
        sonarr_api.secrets,
    ).chmod_folder == ChmodFolder(attr_value)


@pytest.mark.parametrize("attr_value", [None, "", "sonarr"])
def test_chown_group(sonarr_api, attr_value) -> None:
    """
    Check that the `chown_group` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "chownGroup": attr_value})
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).chown_group == (
        attr_value or None
    )


@pytest.mark.parametrize(
    "api_root_folders",
    [
        [],
        [{"id": 0, "path": "/opt/media/downloads"}],
        [{"id": 0, "path": "/opt/media/shows"}, {"id": 1, "path": "/opt/media/anime"}],
    ],
)
def test_root_folders(sonarr_api, api_root_folders) -> None:
    """
    Check that the `root_folders` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        api_root_folders,
    )

    assert SonarrMediaManagementSettingsConfig.from_remote(sonarr_api.secrets).root_folders == set(
        (rf["path"] for rf in api_root_folders),
    )
