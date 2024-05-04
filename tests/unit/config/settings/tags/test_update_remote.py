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
Test the `update_remote` method on the Tags Settings configuration model.
"""

from __future__ import annotations

import pytest

from buildarr_sonarr.config.tags import SonarrTagsSettingsConfig as TagsSettings


@pytest.mark.parametrize("tags", [[], ["shows"], ["shows", "anime"]])
def test_unchanged(sonarr_api, tags) -> None:
    """
    Test that no changes are made when all of the locally defined tags
    exist on the remote instance.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/tag",
        method="GET",
    ).respond_with_json(
        [{"id": 0, "label": "torrent"}] + [{"id": i, "label": t} for i, t in enumerate(tags, 1)],
    )

    assert not TagsSettings(definitions=tags).update_remote(
        tree="sonarr.tags",
        secrets=sonarr_api.secrets,
        remote=TagsSettings(definitions=tags),
    )


@pytest.mark.parametrize("tags", [["shows"], ["shows", "anime"]])
def test_create(sonarr_api, tags) -> None:
    """
    Test creating a new set of tags on the remote instance.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/tag",
        method="GET",
    ).respond_with_json([{"id": 0, "label": "torrent"}])
    for i, tag in enumerate(sorted(tags), 1):
        sonarr_api.server.expect_ordered_request(
            "/api/v3/tag",
            method="POST",
            json={"label": tag},
        ).respond_with_json([{"id": i, "label": tag}], status=201)

    assert TagsSettings(definitions=tags).update_remote(
        tree="sonarr.tags",
        secrets=sonarr_api.secrets,
        remote=TagsSettings(definitions={"torrent"}),
    )
