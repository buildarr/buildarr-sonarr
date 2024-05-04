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
Test the `from_remote` class method on the Tags Settings configuration model.
"""

from __future__ import annotations

import pytest

from buildarr_sonarr.config.tags import SonarrTagsSettingsConfig as TagsSettings


@pytest.mark.parametrize("tags", [[], ["shows"], ["shows", "anime"]])
def test_definitions(sonarr_api, tags) -> None:
    """
    Test that the retrieved set of tags matches the expected value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/tag",
        method="GET",
    ).respond_with_json([{"id": i, "label": t} for i, t in enumerate(tags)])

    assert TagsSettings.from_remote(sonarr_api.secrets).definitions == set(tags)
