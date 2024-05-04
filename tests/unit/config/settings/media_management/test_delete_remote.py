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
Test the `delete_remote` method on the Media Management configuration model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from buildarr_sonarr.config.media_management import (
    SonarrMediaManagementSettingsConfig as MediaManagementSettings,
)

if TYPE_CHECKING:
    from typing import Any, Dict


@pytest.mark.parametrize("root_folders_managed", [False, True])
def test_delete_unmanaged_root_folders_false(sonarr_api, root_folders_managed) -> None:
    """
    Check that root folders on the remote instance that are not defined
    in the local instance configuration are **not** deleted when
    `delete_unmanaged_root_folders` is `false`.
    """

    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [{"id": 0, "path": "/opt/media/shows"}],
    )

    attrs: Dict[str, Any] = {"delete_unmanaged_root_folders": False}
    if root_folders_managed:
        attrs["root_folders"] = set()

    assert not MediaManagementSettings(**attrs).delete_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(
            root_folders={"/opt/media/shows"},
        ),
    )


@pytest.mark.parametrize("api_root_folders", [[], [{"id": 0, "path": "/opt/media/shows"}]])
def test_delete_unmanaged_root_folders_true_unchanged(sonarr_api, api_root_folders) -> None:
    """
    Check that no root folders on the remote instance are deleted
    when the local instance configuration is identical,
    even when `delete_unmanaged_root_folders` is `true`.
    """

    root_folders = set(rf["path"] for rf in api_root_folders)

    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        api_root_folders,
    )

    assert not MediaManagementSettings(
        delete_unmanaged_root_folders=True,
        root_folders=root_folders,
    ).delete_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(
            root_folders=root_folders,
        ),
    )


@pytest.mark.parametrize("api_root_folders", [[], [{"id": 0, "path": "/opt/media/shows"}]])
def test_delete_unmanaged_root_folders_true_changed(sonarr_api, api_root_folders) -> None:
    """
    Check that root folders on the remote instance that are not defined
    in the local instance configuration are deleted when
    `delete_unmanaged_root_folders` is `true`.
    """

    root_folders = set(rf["path"] for rf in api_root_folders)

    sonarr_api.server.expect_ordered_request("/api/v3/rootfolder", method="GET").respond_with_json(
        [*api_root_folders, {"id": 1, "path": "/opt/media/anime"}],
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/rootfolder/1",
        method="DELETE",
    ).respond_with_data(status=200)

    assert MediaManagementSettings(  # type: ignore[call-arg]
        delete_unmanaged_root_folders=True,
        root_folders=root_folders,
    ).delete_remote(
        tree="sonarr.settings.media_management",
        secrets=sonarr_api.secrets,
        remote=MediaManagementSettings(  # type: ignore[call-arg]
            root_folders=root_folders | {"/opt/media/anime"},  # type: ignore[arg-type]
        ),
    )
