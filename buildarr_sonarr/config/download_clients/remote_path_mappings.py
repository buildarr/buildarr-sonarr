# Copyright (C) 2023 Callum Dickinson
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
Sonarr plugin download client remote path mappings.
"""

from __future__ import annotations

from logging import getLogger
from typing import Any, ClassVar, Dict, List, Mapping, Tuple

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from pydantic import field_validator
from typing_extensions import Self

from ...api import api_delete, api_get, api_post, api_put
from ...secrets import SonarrSecrets
from ...types import OSAgnosticPath
from ..types import SonarrConfigBase

logger = getLogger(__name__)


class Ensure(BaseEnum):
    """
    Resource 'ensure' value enumeration.

    Values:

    * `present` (ensure the resource is created if it does not exist)
    * `absent` (ensure the resource is deleted if it exists)
    """

    present = "present"
    absent = "absent"

    def __repr__(self) -> str:
        return repr(self.name)


class RemotePathMapping(SonarrConfigBase):
    """
    Remote path mapping definitions themselves are relatively simple.

    They can be configured with a desired `ensure` state, however, which
    Buildarr uses to control whether to create or delete the remote path mapping.
    Ensure this value is set appropriately.
    """

    host: NonEmptyStr
    """
    The name of the host, as specified for the remote download client.
    """

    remote_path: OSAgnosticPath
    """
    Root path to the directory that the download client accesses.

    *Changed in version 0.6.4*: Path checking will now match paths
    whether or not the defined path ends in a trailing slash.
    Path checking on Windows paths is now case-insensitive.
    """

    local_path: OSAgnosticPath
    """
    The path that Sonarr should use to access the remote path locally.

    *Changed in version 0.6.4*: Path checking will now match paths
    whether or not the defined path ends in a trailing slash.
    Path checking on Windows paths is now case-insensitive.
    """

    ensure: Ensure = Ensure.present
    """
    Desired state for this resource.

    If set to `present`, the resource is created on the remote instance if it does not exist.

    If set to `absent`, the resource will be destroyed on the remote instance if it exists.
    This takes effect even if the  `delete_unmanaged` is set to `False`
    for all remote path mappings.
    """

    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("host", "host", {}),
        ("remote_path", "remotePath", {}),
        ("local_path", "localPath", {}),
    ]

    @field_validator("remote_path", "local_path")
    @classmethod
    def add_trailing_slash(cls, value: OSAgnosticPath) -> OSAgnosticPath:
        if value.is_windows():
            return (value + "\\") if not value.endswith("\\\\") else value
        return (value + "/") if not value.endswith("/") else value

    @classmethod
    def _from_remote(cls, remote_attrs: Mapping[str, Any]) -> Self:
        return cls(**cls.get_local_attrs(cls._remote_map, remote_attrs))

    def _create_remote(self, tree: str, secrets: SonarrSecrets) -> None:
        api_post(
            secrets,
            "/api/v3/remotepathmapping",
            self.get_create_remote_attrs(tree, self._remote_map),
        )

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        remotepathmapping_id: int,
    ) -> bool:
        updated, remote_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._remote_map,
            check_unmanaged=True,
            set_unchanged=True,
        )
        if updated:
            api_put(
                secrets,
                f"/api/v3/remotepathmapping/{remotepathmapping_id}",
                {"id": remotepathmapping_id, **remote_attrs},
            )
            return True
        return False

    def _delete_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remotepathmapping_id: int,
        delete: bool,
    ) -> bool:
        self.log_delete_remote_attrs(tree=tree, remote_map=self._remote_map, delete=delete)
        if delete:
            api_delete(secrets, f"/api/v3/remotepathmapping/{remotepathmapping_id}")
            return True
        return False


class SonarrRemotePathMappingsSettingsConfig(SonarrConfigBase):
    """
    Remote path mappings are used to associate a path on a download client remote host
    with its associated path on the local Sonarr instance.

    The main use case for this is when Sonarr and the download client are not running
    on the same system, or when Docker is used to isolate these services and the
    mountpoints for media locations are not consistent between the containers.

    ```yaml
    sonarr:
      settings:
        download_clients:
          definitions:
            Transmission:
              type: "transmission"
              host: "transmission"
              port: 9091
          remote_path_mappings:
            delete_unmanaged: false # Optional
            definitions:
              - host: "transmission"
                remote_path: "/remote/path"
                local_path: "/local/path"
                ensure: "present" # Optional
    ```

    Remote path mappings can be difficult to properly configure.
    TRaSH-Guides provides an
    [excellent guide](https://trash-guides.info/Sonarr/Sonarr-remote-path-mapping/)
    that explains what they are for, and how to use them.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete remote path mappings not configured in Buildarr.

    Deleting existing remote path mappings can cause problems with a running
    Sonarr instance. Think carefully before you enable this option.
    """

    # TODO: validator to ensure every mapping is unique
    definitions: List[RemotePathMapping] = []
    """
    Remote path mapping definitions.
    """

    @classmethod
    def _from_remote(cls, secrets: SonarrSecrets) -> Self:
        return cls(
            definitions=sorted(
                (
                    RemotePathMapping._from_remote(rpm)
                    for rpm in api_get(secrets, "/api/v3/remotepathmapping")
                ),
                key=lambda v: (v.host, v.remote_path, v.local_path),
            ),
        )

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
    ) -> bool:
        # Track whether remote resource path mappings have been updated.
        changed = False
        # Get required resource IDs from the remote, and create
        # data structures.
        remote_rpm_ids: Dict[Tuple[str, OSAgnosticPath, OSAgnosticPath], int] = {
            (
                rpm["host"],
                OSAgnosticPath(rpm["remotePath"]),
                OSAgnosticPath(rpm["localPath"]),
            ): rpm["id"]
            for rpm in api_get(secrets, "/api/v3/remotepathmapping")
        }
        remote_rpms: Dict[Tuple[str, OSAgnosticPath, OSAgnosticPath], RemotePathMapping] = {
            (rpm.host, rpm.remote_path, rpm.local_path): rpm for rpm in remote.definitions
        }
        # Handle managed remote path mappings.
        for i, rpm in enumerate(self.definitions):
            rpm_tree = f"{tree}.definitions[{i}]"
            rpm_tuple = (rpm.host, rpm.remote_path, rpm.local_path)
            # If the remote path mapping should exist, check that it does,
            # and if not, create it.
            if rpm.ensure == Ensure.present:
                if rpm_tuple in remote_rpms:
                    logger.debug("%s: %s (exists)", rpm_tree, repr(rpm))
                else:
                    rpm._create_remote(tree=rpm_tree, secrets=secrets)
                    changed = True
            # If the remote path mapping should not exist, check that it does not
            # exist in the remote, and if it does, delete it.
            elif rpm_tuple in remote_rpms:
                rpm._delete_remote(
                    tree=rpm_tree,
                    secrets=secrets,
                    remotepathmapping_id=remote_rpm_ids[rpm_tuple],
                    delete=True,
                )
                changed = True
            else:
                logger.debug("%s: %s (does not exist)", rpm_tree, repr(rpm))
        # Return changed status.
        return changed

    def _delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        changed = False
        remote_rpm_ids: Dict[Tuple[str, OSAgnosticPath, OSAgnosticPath], int] = {
            (
                rpm["host"],
                OSAgnosticPath(rpm["remotePath"]),
                OSAgnosticPath(rpm["localPath"]),
            ): rpm["id"]
            for rpm in api_get(secrets, "/api/v3/remotepathmapping")
        }
        local_rpms: Dict[Tuple[str, OSAgnosticPath, OSAgnosticPath], RemotePathMapping] = {
            (rpm.host, rpm.remote_path, rpm.local_path): rpm for rpm in self.definitions
        }
        i = -1
        for rpm in remote.definitions:
            rpm_tuple = (rpm.host, rpm.remote_path, rpm.local_path)
            if rpm_tuple not in local_rpms:
                rpm_tree = f"{tree}.definitions[{i}]"
                if rpm._delete_remote(
                    tree=rpm_tree,
                    secrets=secrets,
                    remotepathmapping_id=remote_rpm_ids[rpm_tuple],
                    delete=self.delete_unmanaged,
                ):
                    changed = True
                i -= 1
        return changed
