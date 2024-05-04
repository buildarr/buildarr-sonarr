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
Test the `update_remote` method on the Metadata Settings configuration model.
"""

from __future__ import annotations

from itertools import product

import pytest

from buildarr_sonarr.config.metadata import (
    KodiEmbyMetadata,
    RoksboxMetadata,
    SonarrMetadataSettingsConfig as MetadataSettings,
    WdtvMetadata,
)

from .util import (
    METADATA_DEFAULTS,
    ROKSBOX_METADATA_DEFAULTS,
    WDTV_METADATA_DEFAULTS,
    XBMC_METADATA_DEFAULTS,
)


def test_defaults(sonarr_api) -> None:
    """
    Check that if the local and remote instance configuration are identical,
    no changes are pushed to the remote instance, and the method reports that
    the configuration is up to date.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(list(METADATA_DEFAULTS.values()))

    # The local configuration is created this way to make Pydantic
    # register all of the values as "set", and therefore Buildarr
    # will consider them "managed" when looking for changes.
    assert not MetadataSettings(
        kodi_emby=KodiEmbyMetadata(**KodiEmbyMetadata().model_dump()),
        roksbox=RoksboxMetadata(**RoksboxMetadata().model_dump()),
        wdtv=WdtvMetadata(**WdtvMetadata().model_dump()),
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_series_metadata(sonarr_api, attr_value) -> None:
    """
    Check that the Kodi/Emby metadata `series_metadata` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **XBMC_METADATA_DEFAULTS,
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "seriesMetadata" else f)
            for f in XBMC_METADATA_DEFAULTS["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            {
                **XBMC_METADATA_DEFAULTS,
                "fields": [
                    ({**f, "value": not attr_value} if f["name"] == "seriesMetadata" else f)
                    for f in XBMC_METADATA_DEFAULTS["fields"]
                ],
            },
            ROKSBOX_METADATA_DEFAULTS,
            WDTV_METADATA_DEFAULTS,
        ],
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata/0",
        method="PUT",
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        kodi_emby=KodiEmbyMetadata(series_metadata=attr_value),
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            kodi_emby=KodiEmbyMetadata(series_metadata=not attr_value),
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_series_metadata_url(sonarr_api, attr_value) -> None:
    """
    Check that the Kodi/Emby metadata `series_metadata_url` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **XBMC_METADATA_DEFAULTS,
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "seriesMetadataUrl" else f)
            for f in XBMC_METADATA_DEFAULTS["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            {
                **XBMC_METADATA_DEFAULTS,
                "fields": [
                    ({**f, "value": not attr_value} if f["name"] == "seriesMetadataUrl" else f)
                    for f in XBMC_METADATA_DEFAULTS["fields"]
                ],
            },
            ROKSBOX_METADATA_DEFAULTS,
            WDTV_METADATA_DEFAULTS,
        ],
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata/0",
        method="PUT",
        json=api_metadata,
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        kodi_emby=KodiEmbyMetadata(series_metadata_url=attr_value),
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            kodi_emby=KodiEmbyMetadata(series_metadata_url=not attr_value),
        ),
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_episode_metadata(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `episode_metadata` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **METADATA_DEFAULTS[metadata_type],
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "episodeMetadata" else f)
            for f in METADATA_DEFAULTS[metadata_type]["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": not attr_value} if f["name"] == "episodeMetadata" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )
    sonarr_api.server.expect_ordered_request(
        f"/api/v3/metadata/{METADATA_DEFAULTS[metadata_type]['id']}",
        method="PUT",
        json=api_metadata,
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        **{metadata_type: {"episode_metadata": attr_value}},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            **{metadata_type: {"episode_metadata": not attr_value}},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_series_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `series_images` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **METADATA_DEFAULTS[metadata_type],
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "seriesImages" else f)
            for f in METADATA_DEFAULTS[metadata_type]["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": not attr_value} if f["name"] == "seriesImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )
    sonarr_api.server.expect_ordered_request(
        f"/api/v3/metadata/{METADATA_DEFAULTS[metadata_type]['id']}",
        method="PUT",
        json=api_metadata,
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        **{metadata_type: {"series_images": attr_value}},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            **{metadata_type: {"series_images": not attr_value}},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_season_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `season_images` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **METADATA_DEFAULTS[metadata_type],
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "seasonImages" else f)
            for f in METADATA_DEFAULTS[metadata_type]["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": not attr_value} if f["name"] == "seasonImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )
    sonarr_api.server.expect_ordered_request(
        f"/api/v3/metadata/{METADATA_DEFAULTS[metadata_type]['id']}",
        method="PUT",
        json=api_metadata,
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        **{metadata_type: {"season_images": attr_value}},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            **{metadata_type: {"season_images": not attr_value}},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize(
    "metadata_type,attr_value",
    product(["kodi_emby", "roksbox", "wdtv"], [False, True]),
)
def test_episode_images(sonarr_api, metadata_type, attr_value) -> None:
    """
    Check that the general metadata `episode_images` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_metadata = {
        **METADATA_DEFAULTS[metadata_type],
        "fields": [
            ({**f, "value": attr_value} if f["name"] == "episodeImages" else f)
            for f in METADATA_DEFAULTS[metadata_type]["fields"]
        ],
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/metadata",
        method="GET",
    ).respond_with_json(
        [
            (
                {
                    **metadata,
                    "fields": [
                        ({**f, "value": not attr_value} if f["name"] == "episodeImages" else f)
                        for f in metadata["fields"]
                    ],
                }
                if mt == metadata_type
                else metadata
            )
            for mt, metadata in METADATA_DEFAULTS.items()
        ],
    )
    sonarr_api.server.expect_ordered_request(
        f"/api/v3/metadata/{METADATA_DEFAULTS[metadata_type]['id']}",
        method="PUT",
        json=api_metadata,
    ).respond_with_json(api_metadata, status=202)

    assert MetadataSettings(
        **{metadata_type: {"episode_images": attr_value}},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.metadata",
        secrets=sonarr_api.secrets,
        remote=MetadataSettings(
            **{metadata_type: {"episode_images": not attr_value}},  # type: ignore[arg-type]
        ),
    )
