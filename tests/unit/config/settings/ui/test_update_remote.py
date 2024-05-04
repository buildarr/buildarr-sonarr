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
Test the `update_remote` method on the UI Settings configuration model.
"""

from __future__ import annotations

import pytest

from buildarr_sonarr.config.ui import (
    FirstDayOfWeek,
    LongDateFormat,
    ShortDateFormat,
    SonarrUISettingsConfig as UISettings,
    TimeFormat,
    WeekColumnHeader,
)

from .util import UI_CONFIG_DEFAULTS


def test_defaults(sonarr_api) -> None:
    """
    Check that if the local and remote instance configuration are identical,
    no changes are pushed to the remote instance, and the method reports that
    the configuration is up to date.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(UI_CONFIG_DEFAULTS)

    # The local configuration is created this way to make Pydantic
    # register all of the values as "set", and therefore Buildarr
    # will consider them "managed" when looking for changes.
    assert not UISettings(**UISettings().model_dump()).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(),
    )


@pytest.mark.parametrize("attr_value", [0, 1])
def test_first_day_of_week(sonarr_api, attr_value) -> None:
    """
    Check that the `first_day_of_week` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "firstDayOfWeek": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(
        {
            **UI_CONFIG_DEFAULTS,
            "firstDayOfWeek": 0 if attr_value else 1,
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(first_day_of_week=FirstDayOfWeek(attr_value)).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(
            first_day_of_week=FirstDayOfWeek.sunday if attr_value else FirstDayOfWeek.monday,
        ),
    )


@pytest.mark.parametrize("attr_value", ["ddd M/D", "ddd MM/DD", "ddd D/M", "ddd DD/MM"])
def test_week_column_header(sonarr_api, attr_value) -> None:
    """
    Check that the `week_column_header` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "calendarWeekColumnHeader": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(
        {
            **UI_CONFIG_DEFAULTS,
            "calendarWeekColumnHeader": "ddd D/M" if attr_value == "ddd M/D" else "ddd M/D",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(week_column_header=WeekColumnHeader(attr_value)).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(
            week_column_header=(
                WeekColumnHeader.day_first
                if attr_value == "ddd M/D"
                else WeekColumnHeader.month_first
            ),
        ),
    )


@pytest.mark.parametrize(
    "attr_value",
    ["MMM D YYYY", "DD MMM YYYY", "MM/D/YYYY", "MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
)
def test_short_date_format(sonarr_api, attr_value) -> None:
    """
    Check that the `short_date_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "shortDateFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(
        {
            **UI_CONFIG_DEFAULTS,
            "shortDateFormat": "YYYY-MM-DD" if attr_value == "MMM D YYYY" else "MMM D YYYY",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(short_date_format=ShortDateFormat(attr_value)).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(
            short_date_format=(
                ShortDateFormat.iso8601
                if attr_value == "MMM D YYYY"
                else ShortDateFormat.word_month_first
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", ["dddd, MMMM D YYYY", "dddd, D MMMM YYYY"])
def test_long_date_format(sonarr_api, attr_value) -> None:
    """
    Check that the `long_date_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "longDateFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(
        {
            **UI_CONFIG_DEFAULTS,
            "longDateFormat": (
                "dddd, D MMMM YYYY" if attr_value == "dddd, MMMM D YYYY" else "dddd, MMMM D YYYY"
            ),
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(long_date_format=LongDateFormat(attr_value)).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(
            long_date_format=(
                LongDateFormat.day_first
                if attr_value == "dddd, MMMM D YYYY"
                else LongDateFormat.month_first
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", ["h(:mm)a", "HH:mm"])
def test_time_format(sonarr_api, attr_value) -> None:
    """
    Check that the `time_format` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "timeFormat": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(
        {
            **UI_CONFIG_DEFAULTS,
            "timeFormat": "h(:mm)a" if attr_value == "HH:mm" else "HH:mm",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(time_format=TimeFormat(attr_value)).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(
            time_format=(
                TimeFormat.twelve_hour if attr_value == "HH:mm" else TimeFormat.twentyfour_hour
            ),
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_show_relative_dates(sonarr_api, attr_value) -> None:
    """
    Check that the `show_relative_dates` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "showRelativeDates": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "showRelativeDates": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(show_relative_dates=attr_value).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(show_relative_dates=not attr_value),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_enable_color_impaired_mode(sonarr_api, attr_value) -> None:
    """
    Check that the `enable_color_impaired_mode` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_ui_config = {**UI_CONFIG_DEFAULTS, "enableColorImpairedMode": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "enableColorImpairedMode": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui/0",
        method="PUT",
        json=api_ui_config,
    ).respond_with_json(api_ui_config, status=202)

    assert UISettings(enable_color_impaired_mode=attr_value).update_remote(
        tree="sonarr.settings.ui",
        secrets=sonarr_api.secrets,
        remote=UISettings(enable_color_impaired_mode=not attr_value),
    )
