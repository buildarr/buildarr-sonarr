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
Sonarr plugin configuration.
"""


from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from buildarr.config import ConfigPlugin
from buildarr.types import NonEmptyStr, Port
from pydantic import validator
from typing_extensions import Self

from ..types import SonarrApiKey, SonarrProtocol
from .connect import SonarrConnectSettingsConfig
from .download_clients import SonarrDownloadClientsSettingsConfig
from .general import SonarrGeneralSettingsConfig
from .import_lists import SonarrImportListsSettingsConfig
from .indexers import SonarrIndexersSettingsConfig
from .media_management import SonarrMediaManagementSettingsConfig
from .metadata import SonarrMetadataSettingsConfig
from .profiles import SonarrProfilesSettingsConfig
from .quality import SonarrQualitySettingsConfig
from .tags import SonarrTagsSettingsConfig
from .types import SonarrConfigBase
from .ui import SonarrUISettingsConfig

if TYPE_CHECKING:
    from ..secrets import SonarrSecrets

    class _SonarrInstanceConfig(ConfigPlugin[SonarrSecrets]):
        ...

else:

    class _SonarrInstanceConfig(ConfigPlugin):
        ...


class SonarrSettingsConfig(SonarrConfigBase):
    """
    Sonarr settings, used to configure a remote Sonarr instance.
    """

    media_management = SonarrMediaManagementSettingsConfig()  # type: ignore[call-arg]
    profiles = SonarrProfilesSettingsConfig()
    quality = SonarrQualitySettingsConfig()
    indexers = SonarrIndexersSettingsConfig()  # type: ignore[call-arg]
    download_clients = SonarrDownloadClientsSettingsConfig()
    import_lists = SonarrImportListsSettingsConfig()
    connect = SonarrConnectSettingsConfig()
    metadata = SonarrMetadataSettingsConfig()
    tags = SonarrTagsSettingsConfig()
    general = SonarrGeneralSettingsConfig()
    ui = SonarrUISettingsConfig()

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # Overload base function to guarantee execution order of section updates.
        # 1. Tags must be created before everything else.
        # 2. Qualities must be updated before quality profiles.
        # 3. Download clients must be created before indexers.
        # 4. Indexers must be created before release profiles.
        return any(
            [
                self.tags.update_remote(
                    f"{tree}.tags",
                    secrets,
                    remote.tags,
                    check_unmanaged=check_unmanaged,
                ),
                self.quality.update_remote(
                    f"{tree}.quality",
                    secrets,
                    remote.quality,
                    check_unmanaged=check_unmanaged,
                ),
                self.download_clients.update_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                    check_unmanaged=check_unmanaged,
                ),
                self.indexers.update_remote(
                    f"{tree}.indexers",
                    secrets,
                    remote.indexers,
                    check_unmanaged=check_unmanaged,
                ),
                self.media_management.update_remote(
                    f"{tree}.media_management",
                    secrets,
                    remote.media_management,
                    check_unmanaged=check_unmanaged,
                ),
                self.profiles.update_remote(
                    f"{tree}.profiles",
                    secrets,
                    remote.profiles,
                    check_unmanaged=check_unmanaged,
                ),
                self.import_lists.update_remote(
                    f"{tree}.import_lists",
                    secrets,
                    remote.import_lists,
                    check_unmanaged=check_unmanaged,
                ),
                self.connect.update_remote(
                    f"{tree}.connect",
                    secrets,
                    remote.connect,
                    check_unmanaged=check_unmanaged,
                ),
                self.metadata.update_remote(
                    f"{tree}.metadata",
                    secrets,
                    remote.metadata,
                    check_unmanaged=check_unmanaged,
                ),
                self.general.update_remote(
                    f"{tree}.general",
                    secrets,
                    remote.general,
                    check_unmanaged=check_unmanaged,
                ),
                self.ui.update_remote(
                    f"{tree}.ui",
                    secrets,
                    remote.ui,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )

    def delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        # Overload base function to guarantee execution order of section deletions.
        # 1. Release profiles must be deleted before indexers.
        # 2. Indexers must be deleted before download clients.
        return any(
            [
                self.profiles.delete_remote(f"{tree}.profiles", secrets, remote.profiles),
                self.indexers.delete_remote(f"{tree}.indexers", secrets, remote.indexers),
                self.download_clients.delete_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                ),
                self.media_management.delete_remote(
                    f"{tree}.media_management",
                    secrets,
                    remote.media_management,
                ),
                self.import_lists.delete_remote(
                    f"{tree}.import_lists",
                    secrets,
                    remote.import_lists,
                ),
                self.connect.delete_remote(f"{tree}.connect", secrets, remote.connect),
                self.tags.delete_remote(f"{tree}.tags", secrets, remote.tags),
                self.quality.delete_remote(f"{tree}.quality", secrets, remote.quality),
                self.metadata.delete_remote(f"{tree}.metadata", secrets, remote.metadata),
                self.general.delete_remote(f"{tree}.general", secrets, remote.general),
                self.ui.delete_remote(f"{tree}.ui", secrets, remote.ui),
            ],
        )


class SonarrInstanceConfig(_SonarrInstanceConfig):
    """
    By default, Buildarr will look for a single instance at `http://sonarr:8989`.
    Most configurations are different, and to accommodate those, you can configure
    how Buildarr connects to individual Sonarr instances.

    Configuration of a single Sonarr instance:

    ```yaml
    sonarr:
      hostname: "sonarr.example.com"
      port: 8989
      protocol: "http"
      settings:
        ...
    ```

    Configuration of multiple instances:

    ```yaml
    sonarr:
      # Configuration and settings common to all instances.
      port: 8989
      settings:
        ...
      instances:
        # Sonarr instance 1-specific configuration.
        sonarr1:
          hostname: "sonarr1.example.com"
          settings:
            ...
        # Sonarr instance 2-specific configuration.
        sonarr2:
          hostname: "sonarr2.example.com"
          api_key: "..." # Explicitly define API key
          settings:
            ...
    ```
    """

    hostname: NonEmptyStr = "sonarr"  # type: ignore[assignment]
    """
    Hostname of the Sonarr instance to connect to.

    When defining a single instance using the global `sonarr` configuration block,
    the default hostname is `sonarr`.

    When using multiple instance-specific configurations, the default hostname
    is the name given to the instance in the `instances` attribute.

    ```yaml
    sonarr:
      instances:
        sonarr1: # <--- This becomes the default hostname
          ...
    ```
    """

    port: Port = 8989  # type: ignore[assignment]
    """
    Port number of the Sonarr instance to connect to.
    """

    protocol: SonarrProtocol = "http"  # type: ignore[assignment]
    """
    Communication protocol to use to connect to Sonarr.
    """

    url_base: Optional[str] = None
    """
    The URL path the Sonarr instance API is available under, if behind a reverse proxy.

    API URLs are rendered like this: `<protocol>://<hostname>:<port><url_base>/api/v3/...`

    When unset, the URL root will be used as the API endpoint
    (e.g. `<protocol>://<hostname>:<port>/api/v3/...`).

    *Added in version 0.6.3.*
    """

    api_key: Optional[SonarrApiKey] = None
    """
    API key to use to authenticate with the Sonarr instance.

    If undefined or set to `None`, automatically retrieve the API key.
    This can only be done on Sonarr instances with authentication disabled.
    """

    image: NonEmptyStr = "lscr.io/linuxserver/sonarr"  # type: ignore[assignment]
    """
    The default Docker image URI when generating a Docker Compose file.
    """

    version: Optional[str] = None
    """
    The expected version of the Sonarr instance.
    If undefined or set to `None`, the version is auto-detected.

    This value is also used when generating a Docker Compose file.
    When undefined or set to `None`, the version tag will be set to `latest`.
    """

    settings: SonarrSettingsConfig = SonarrSettingsConfig()
    """
    Sonarr settings.
    Configuration options for Sonarr itself are set within this structure.
    """

    @validator("url_base")
    def validate_url_base(cls, value: Optional[str]) -> Optional[str]:
        return f"/{value.strip('/')}" if value and value.strip("/") else None

    def uses_trash_metadata(self) -> bool:
        if self.settings.quality.uses_trash_metadata():
            return True
        for release_profile in self.settings.profiles.release_profiles.definitions.values():
            if release_profile.uses_trash_metadata():
                return True
        return False

    def render(self) -> Self:
        if not self.uses_trash_metadata():
            return self
        copy = self.copy(deep=True)
        copy._render()
        return copy

    def _render(self) -> None:
        for rp in self.settings.profiles.release_profiles.definitions.values():
            if rp.uses_trash_metadata():
                rp._render()
        if self.settings.quality.uses_trash_metadata():
            self.settings.quality._render()

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        """
        Read configuration from a remote instance and return it as a configuration object.

        Args:
            secrets (SonarrSecrets): Instance host and secrets information

        Returns:
            Configuration object for remote instance
        """
        return cls(
            hostname=secrets.hostname,
            port=secrets.port,
            protocol=secrets.protocol,
            url_base=secrets.url_base,
            api_key=secrets.api_key,
            version=secrets.version,
            settings=SonarrSettingsConfig.from_remote(secrets),
        )

    def to_compose_service(self, compose_version: str, service_name: str) -> Dict[str, Any]:
        return {
            "image": f"{self.image}:{self.version or 'latest'}",
            "volumes": {service_name: "/config"},
        }


class SonarrConfig(SonarrInstanceConfig):
    """
    Sonarr plugin global configuration class.
    """

    instances: Dict[str, SonarrInstanceConfig] = {}
    """
    Instance-specific Sonarr configuration.

    Can only be defined on the global `sonarr` configuration block.

    Globally specified configuration values apply to all instances.
    Configuration values specified on an instance-level take precedence at runtime.
    """
