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
Test the `from_remote` class method on the UI Settings configuration model.
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
    Check that providing the default values results in a model object
    that is equal to one created directly.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json(UI_CONFIG_DEFAULTS)

    assert UISettings.from_remote(sonarr_api.secrets) == UISettings()


@pytest.mark.parametrize("attr_value", [0, 1])
def test_first_day_of_week(sonarr_api, attr_value) -> None:
    """
    Check that the `first_day_of_week` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "firstDayOfWeek": attr_value})

    assert UISettings.from_remote(
        sonarr_api.secrets,
    ).first_day_of_week == FirstDayOfWeek(attr_value)


@pytest.mark.parametrize("attr_value", ["ddd M/D", "ddd MM/DD", "ddd D/M", "ddd DD/MM"])
def test_week_column_header(sonarr_api, attr_value) -> None:
    """
    Check that the `week_column_header` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "calendarWeekColumnHeader": attr_value})

    assert UISettings.from_remote(
        sonarr_api.secrets,
    ).week_column_header == WeekColumnHeader(attr_value)


@pytest.mark.parametrize(
    "attr_value",
    ["MMM D YYYY", "DD MMM YYYY", "MM/D/YYYY", "MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
)
def test_short_date_format(sonarr_api, attr_value) -> None:
    """
    Check that the `short_date_format` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "shortDateFormat": attr_value})

    assert UISettings.from_remote(
        sonarr_api.secrets,
    ).short_date_format == ShortDateFormat(attr_value)


@pytest.mark.parametrize("attr_value", ["dddd, MMMM D YYYY", "dddd, D MMMM YYYY"])
def test_long_date_format(sonarr_api, attr_value) -> None:
    """
    Check that the `long_date_format` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "longDateFormat": attr_value})

    assert UISettings.from_remote(
        sonarr_api.secrets,
    ).long_date_format == LongDateFormat(attr_value)


@pytest.mark.parametrize("attr_value", ["h(:mm)a", "HH:mm"])
def test_time_format(sonarr_api, attr_value) -> None:
    """
    Check that the `time_format` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "timeFormat": attr_value})

    assert UISettings.from_remote(
        sonarr_api.secrets,
    ).time_format == TimeFormat(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_show_relative_dates(sonarr_api, attr_value) -> None:
    """
    Check that the `show_relative_dates` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "showRelativeDates": attr_value})

    assert UISettings.from_remote(sonarr_api.secrets).show_relative_dates is attr_value


@pytest.mark.parametrize("attr_value", [False, True])
def test_enable_color_impaired_mode(sonarr_api, attr_value) -> None:
    """
    Check that the `enable_color_impaired_mode` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/ui",
        method="GET",
    ).respond_with_json({**UI_CONFIG_DEFAULTS, "enableColorImpairedMode": attr_value})

    assert UISettings.from_remote(sonarr_api.secrets).enable_color_impaired_mode is attr_value
