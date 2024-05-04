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
Test the `from_remote` class method on the Metadata Settings configuration model.
"""

from __future__ import annotations

from itertools import product

import pytest

from buildarr_sonarr.config.metadata import SonarrMetadataSettingsConfig as MetadataSettings

from .util import (
    METADATA_DEFAULTS,
    ROKSBOX_METADATA_DEFAULTS,
    WDTV_METADATA_DEFAULTS,
    XBMC_METADATA_DEFAULTS,
)


def test_defaults(sonarr_api) -> None:
    """
    Check that fetching the default values from a remote instance
    results in a model object that is equal to one created directly.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(list(METADATA_DEFAULTS.values()))

    assert MetadataSettings.from_remote(sonarr_api.secrets) == MetadataSettings()


@pytest.mark.parametrize("attr_value", [False, True])
def test_series_metadata(sonarr_api, attr_value) -> None:
    """
    Check that the Kodi/Emby metadata `series_metadata` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            {
                **XBMC_METADATA_DEFAULTS,
                "fields": [
                    ({**f, "value": attr_value} if f["name"] == "seriesMetadata" else f)
                    for f in XBMC_METADATA_DEFAULTS["fields"]
                ],
            },
            ROKSBOX_METADATA_DEFAULTS,
            WDTV_METADATA_DEFAULTS,
        ],
    )

    assert MetadataSettings.from_remote(sonarr_api.secrets).kodi_emby.series_metadata is attr_value


@pytest.mark.parametrize("attr_value", [False, True])
def test_series_metadata_url(sonarr_api, attr_value) -> None:
    """
    Check that the Kodi/Emby metadata `series_metadata_url` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            {
                **XBMC_METADATA_DEFAULTS,
                "fields": [
                    ({**f, "value": attr_value} if f["name"] == "seriesMetadataUrl" else f)
                    for f in XBMC_METADATA_DEFAULTS["fields"]
                ],
            },
            ROKSBOX_METADATA_DEFAULTS,
            WDTV_METADATA_DEFAULTS,
        ],
    )

    assert (
        MetadataSettings.from_remote(
            sonarr_api.secrets,
        ).kodi_emby.series_metadata_url
        is attr_value
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_episode_metadata(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `episode_metadata` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": attr_value} if f["name"] == "episodeMetadata" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )

    assert (
        getattr(MetadataSettings.from_remote(sonarr_api.secrets), metadata_type).episode_metadata
        is attr_value
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_series_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `series_images` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": attr_value} if f["name"] == "seriesImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )

    assert (
        getattr(MetadataSettings.from_remote(sonarr_api.secrets), metadata_type).series_images
        is attr_value
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_season_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `season_images` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": attr_value} if f["name"] == "seasonImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )

    assert (
        getattr(MetadataSettings.from_remote(sonarr_api.secrets), metadata_type).season_images
        is attr_value
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_episode_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `episode_images` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": attr_value} if f["name"] == "episodeImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )

    assert (
        getattr(MetadataSettings.from_remote(sonarr_api.secrets), metadata_type).episode_images
        is attr_value
    )
