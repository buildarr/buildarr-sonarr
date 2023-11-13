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
Sonarr plugin secrets file model.
"""


from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, cast
from urllib.parse import urlparse

from buildarr.secrets import SecretsPlugin
from buildarr.types import NonEmptyStr, Port

from .api import api_get, get_initialize_js
from .exceptions import SonarrAPIError, SonarrSecretsUnauthorizedError
from .types import SonarrApiKey, SonarrProtocol

if TYPE_CHECKING:
    from typing import Optional

    from typing_extensions import Self

    from .config import SonarrConfig

    class _SonarrSecrets(SecretsPlugin[SonarrConfig]):
        ...

else:

    class _SonarrSecrets(SecretsPlugin):
        ...


class SonarrSecrets(_SonarrSecrets):
    """
    Sonarr API secrets.
    """

    hostname: NonEmptyStr
    port: Port
    protocol: SonarrProtocol
    api_key: SonarrApiKey

    @property
    def host_url(self) -> str:
        return f"{self.protocol}://{self.hostname}:{self.port}"

    @classmethod
    def from_url(cls, base_url: str, api_key: str) -> Self:
        url_obj = urlparse(base_url)
        hostname_port = url_obj.netloc.rsplit(":", 1)
        hostname = hostname_port[0]
        protocol = url_obj.scheme
        port = (
            int(hostname_port[1])
            if len(hostname_port) > 1
            else (443 if protocol == "https" else 80)
        )
        return cls(
            hostname=cast(NonEmptyStr, hostname),
            port=cast(Port, port),
            protocol=cast(SonarrProtocol, protocol),
            api_key=cast(SonarrApiKey, api_key),
        )

    @classmethod
    def get(cls, config: SonarrConfig) -> Self:
        return cls.get_from_url(
            hostname=config.hostname,
            port=config.port,
            protocol=config.protocol,
            api_key=config.api_key.get_secret_value() if config.api_key else None,
        )

    @classmethod
    def get_from_url(
        cls,
        hostname: str,
        port: int,
        protocol: str,
        api_key: Optional[str] = None,
    ) -> Self:
        host_url = f"{protocol}://{hostname}:{port}"
        if not api_key:
            try:
                initialize_js = get_initialize_js(host_url)
            except SonarrAPIError as err:
                if err.status_code == HTTPStatus.UNAUTHORIZED:
                    raise SonarrSecretsUnauthorizedError(
                        (
                            "Unable to retrieve the API key for the Sonarr instance "
                            f"at '{host_url}': Authentication is enabled. "
                            "Please set the 'Settings -> General -> Authentication' attribute "
                            "to 'None', or if you do not wish to disable authentication, "
                            "explicitly define the API key in the Buildarr configuration."
                        ),
                    ) from None
                else:
                    raise
            else:
                api_key = initialize_js["apiKey"]
        return cls(
            hostname=cast(NonEmptyStr, hostname),
            port=cast(Port, port),
            protocol=cast(SonarrProtocol, protocol),
            api_key=cast(SonarrApiKey, api_key),
        )

    def test(self) -> bool:
        try:
            api_get(self, "/api/v3/system/status")
            return True
        except SonarrAPIError as err:
            if err.status_code == HTTPStatus.UNAUTHORIZED:
                return False
            else:
                raise
