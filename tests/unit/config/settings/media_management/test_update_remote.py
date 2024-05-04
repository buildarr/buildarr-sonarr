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
Test the `update_remote` method on the Media Management configuration model.
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
    SonarrMediaManagementSettingsConfig as MediaManagementSettings,
)

from .util import MEDIAMANAGEMENT_CONFIG_DEFAULTS, NAMING_CONFIG_DEFAULTS


def test_unchanged(sonarr_api) -> None:
    """
    Check that if the local and remote instance configuration are identical,
    no changes are pushed to the remote instance, and the method reports that
    the configuration is up to date.
    """

    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    # The local configuration is created this way to make Pydantic
    # register all of the values as "set", and therefore Buildarr
    # will consider them "managed" when looking for changes.
    assert not MediaManagementSettings(
        **MediaManagementSettings().model_dump(),  # type: ignore[call-arg]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_rename_episodes(sonarr_api, attr_value) -> None:
    """
    Check that the `rename_episodes` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "renameEpisodes": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "renameEpisodes": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        rename_episodes=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(rename_episodes=not attr_value),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_replace_illegal_characters(sonarr_api, attr_value) -> None:
    """
    Check that the `replace_illegal_characters` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "replaceIllegalCharacters": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json({**NAMING_CONFIG_DEFAULTS, "replaceIllegalCharacters": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        replace_illegal_characters=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            replace_illegal_characters=not attr_value,
        ),
    )


def test_standard_episode_format(sonarr_api) -> None:
    """
    Check that the `standard_episode_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "{Series TitleYear} - S{season:00}E{episode:00} - {Episode CleanTitle}"
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "standardEpisodeFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        standard_episode_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


def test_daily_episode_format(sonarr_api) -> None:
    """
    Check that the `daily_episode_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "{Series TitleYear} - {Air-Date} - {Episode CleanTitle}"
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "dailyEpisodeFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        daily_episode_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


def test_anime_episode_format(sonarr_api) -> None:
    """
    Check that the `anime_episode_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = (
        "{Series TitleYear} - S{season:00}E{episode:00} - {absolute:000} - {Episode CleanTitle}"
    )
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "animeEpisodeFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        anime_episode_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


def test_series_folder_format(sonarr_api) -> None:
    """
    Check that the `series_folder_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "{Series Title}"
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "seriesFolderFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        series_folder_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


def test_season_folder_format(sonarr_api) -> None:
    """
    Check that the `season_folder_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "Season {season}"
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "seasonFolderFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        season_folder_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


def test_specials_folder_format(sonarr_api) -> None:
    """
    Check that the `specials_folder_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "Special"
    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "specialsFolderFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        specials_folder_format=attr_value,  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", list(range(6)))
def test_multiepisode_style(sonarr_api, attr_value) -> None:
    """
    Check that the `multiepisode_style` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_naming_config = {**NAMING_CONFIG_DEFAULTS, "multiEpisodeStyle": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming",
        method="GET",
    ).respond_with_json(NAMING_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/naming/0",
        method="PUT",
        json=api_naming_config,
    ).respond_with_json(api_naming_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        multiepisode_style=MultiEpisodeStyle(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            multiepisode_style=(
                MultiEpisodeStyle.range  # Default value.
                if attr_value != 4  # noqa: PLR2004
                else MultiEpisodeStyle.extend  # Set to non-default value if default is tested.
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_create_empty_series_folders(sonarr_api, attr_value) -> None:
    """
    Check that the `create_empty_series_folders` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "createEmptySeriesFolders": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "createEmptySeriesFolders": not attr_value},
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        create_empty_series_folders=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            create_empty_series_folders=not attr_value,
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_delete_empty_folders(sonarr_api, attr_value) -> None:
    """
    Check that the `delete_empty_folders` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "deleteEmptyFolders": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "deleteEmptyFolders": not attr_value},
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        delete_empty_folders=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            delete_empty_folders=not attr_value,
        ),
    )


@pytest.mark.parametrize("attr_value", ["always", "bulkSeasonReleases", "never"])
def test_episode_title_required(sonarr_api, attr_value) -> None:
    """
    Check that the `episode_title_required` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "episodeTitleRequired": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        episode_title_required=EpisodeTitleRequired(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            episode_title_required=(
                EpisodeTitleRequired.always  # Default value.
                if attr_value != "always"
                else EpisodeTitleRequired.never  # Set to non-default value if default is tested.
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_skip_free_space_check(sonarr_api, attr_value) -> None:
    """
    Check that the `skip_free_space_check` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "skipFreeSpaceCheckWhenImporting": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "skipFreeSpaceCheckWhenImporting": not attr_value},
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        skip_free_space_check=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            skip_free_space_check=not attr_value,
        ),
    )


def test_minimum_free_space(sonarr_api) -> None:
    """
    Check that the `minimum_free_space` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 200

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "minimumFreeSpaceWhenImporting": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        minimum_free_space=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_use_hardlinks(sonarr_api, attr_value) -> None:
    """
    Check that the `use_hardlinks` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "copyUsingHardlinks": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "copyUsingHardlinks": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        use_hardlinks=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(use_hardlinks=not attr_value),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_import_extra_files(sonarr_api, attr_value) -> None:
    """
    Check that the `import_extra_files` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "importExtraFiles": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "importExtraFiles": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        import_extra_files=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            import_extra_files=not attr_value,
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_unmonitor_deleted_episodes(sonarr_api, attr_value) -> None:
    """
    Check that the `unmonitor_deleted_episodes` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "autoUnmonitorPreviouslyDownloadedEpisodes": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {
            **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
            "autoUnmonitorPreviouslyDownloadedEpisodes": not attr_value,
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        unmonitor_deleted_episodes=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            unmonitor_deleted_episodes=not attr_value,
        ),
    )


@pytest.mark.parametrize("attr_value", ["preferAndUpgrade", "doNotUpgrade", "doNotPrefer"])
def test_propers_and_repacks(sonarr_api, attr_value) -> None:
    """
    Check that the `propers_and_repacks` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "downloadPropersAndRepacks": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        propers_and_repacks=PropersAndRepacks(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            propers_and_repacks=(
                PropersAndRepacks.do_not_prefer  # Default value.
                if attr_value != "doNotPrefer"
                # Set to non-default value if default is tested.
                else PropersAndRepacks.prefer_and_upgrade
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_analyze_video_files(sonarr_api, attr_value) -> None:
    """
    Check that the `analyze_video_files` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "enableMediaInfo": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "enableMediaInfo": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        analyze_video_files=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            analyze_video_files=not attr_value,
        ),
    )


@pytest.mark.parametrize("attr_value", ["always", "afterManual", "never"])
def test_rescan_series_folder_after_refresh(sonarr_api, attr_value) -> None:
    """
    Check that the `rescan_series_folder_after_refresh` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "rescanAfterRefresh": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        rescan_series_folder_after_refresh=RescanSeriesFolderAfterRefresh(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            rescan_series_folder_after_refresh=(
                RescanSeriesFolderAfterRefresh.always  # Default value.
                if attr_value != "always"
                # Set to non-default value if default is tested.
                else RescanSeriesFolderAfterRefresh.never
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", ["none", "localAirDate", "utcAirDate"])
def test_change_file_date(sonarr_api, attr_value) -> None:
    """
    Check that the `change_file_date` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "fileDate": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        change_file_date=ChangeFileDate(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            change_file_date=(
                ChangeFileDate.none  # Default value.
                if attr_value != "none"
                # Set to non-default value if default is tested.
                else ChangeFileDate.utc_air_date
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [None, "", "/opt/recycling-bin"])
def test_recycling_bin(sonarr_api, attr_value) -> None:
    """
    Check that the `recycling_bin` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "recycleBin": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {
            **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
            "recycleBin": "" if attr_value else "/opt/recycling-bin",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        recycling_bin=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            recycling_bin="/opt/recycling-bin" if not attr_value else None,
        ),
    )


def test_recycling_bin_cleanup(sonarr_api) -> None:
    """
    Check that the `recycling_bin_cleanup` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 30

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "recycleBinCleanupDays": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        recycling_bin_cleanup=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_set_permissions(sonarr_api, attr_value) -> None:
    """
    Check that the `set_permissions` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {
        **MEDIAMANAGEMENT_CONFIG_DEFAULTS,
        "setPermissionsLinux": attr_value,
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json({**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "setPermissionsLinux": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        set_permissions=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(set_permissions=not attr_value),  # type: ignore[call-arg]
    )


@pytest.mark.parametrize("attr_value", ["755", "775", "770", "750", "777"])
def test_chmod_folder(sonarr_api, attr_value) -> None:
    """
    Check that the `chmod_folder` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "chmodFolder": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(MEDIAMANAGEMENT_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        chmod_folder=ChmodFolder(attr_value),
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            chmod_folder=(
                ChmodFolder.drwxrwxrwx  # Default value.
                if attr_value != "777"
                # Set to non-default value if default is tested.
                else ChmodFolder.drwxr_xr_x
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [None, "", "sonarr"])
def test_chown_group(sonarr_api, attr_value) -> None:
    """
    Check that the `chown_group` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_mediamanagement_config = {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "chownGroup": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement",
        method="GET",
    ).respond_with_json(
        {**MEDIAMANAGEMENT_CONFIG_DEFAULTS, "chownGroup": "" if attr_value else "sonarr"},
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/mediamanagement/0",
        method="PUT",
        json=api_mediamanagement_config,
    ).respond_with_json(api_mediamanagement_config, status=202)
    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [],
    )

    assert MediaManagementSettings(  # type: ignore[call-arg]
        chown_group=attr_value,
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            chown_group="sonarr" if not attr_value else None,
        ),
    )


@pytest.mark.parametrize("api_root_folders", [[], [{"id": 0, "path": "/opt/media/shows"}]])
def test_root_folders(sonarr_api, api_root_folders) -> None:
    """
    Check that root folders that do not exist on the remote instance are created.
    """

    root_folders = set(rf["path"] for rf in api_root_folders)

    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        api_root_folders,
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/rootfolder",
        method="POST",
        json={"path": "/opt/media/anime"},
    ).respond_with_json(
        {"id": 1, "path": "/opt/media/anime"},
        status=201,
    )

    assert MediaManagementSettings(
        root_folders=root_folders | {"/opt/media/anime"},
    ).update_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(root_folders=root_folders),
    )
