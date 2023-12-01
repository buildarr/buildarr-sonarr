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
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from buildarr.secrets import SecretsPlugin
from buildarr.types import NonEmptyStr, Port
from pydantic import validator

from .api import api_get, get_initialize_js
from .exceptions import SonarrAPIError, SonarrSecretsUnauthorizedError
from .types import SonarrApiKey, SonarrProtocol

if TYPE_CHECKING:
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
    url_base: Optional[str]
    api_key: SonarrApiKey
    version: NonEmptyStr

    @property
    def host_url(self) -> str:
        return f"{self.protocol}://{self.hostname}:{self.port}{self.url_base or ''}"

    @validator("url_base")
    def validate_url_base(cls, value: Optional[str]) -> Optional[str]:
        return f"/{value.strip('/')}" if value and value.strip("/") else None

    @classmethod
    def get(cls, config: SonarrConfig) -> Self:
        return cls.get_from_url(
            hostname=config.hostname,
            port=config.port,
            protocol=config.protocol,
            url_base=config.url_base,
            api_key=config.api_key.get_secret_value() if config.api_key else None,
        )

    @classmethod
    def get_from_url(
        cls,
        hostname: str,
        port: int,
        protocol: str,
        url_base: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> Self:
        _url_base = cls.validate_url_base(url_base)
        host_url = f"{protocol}://{hostname}:{port}{_url_base or ''}"
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
        try:
            system_status = cast(
                Dict[str, Any],
                api_get(host_url, "/api/v3/system/status", api_key=api_key),
            )
        except SonarrAPIError as err:
            if err.status_code == HTTPStatus.UNAUTHORIZED:
                raise SonarrSecretsUnauthorizedError(
                    (
                        f"Incorrect API key for the Sonarr instance at '{host_url}'. "
                        "Please check that the API key is set correctly in the Buildarr "
                        "configuration, and that it is set to the value as shown in "
                        "'Settings -> General -> API Key' on the Radarr instance."
                    ),
                ) from None
            else:
                raise
        try:
            version = cast(NonEmptyStr, system_status["version"])
        except KeyError:
            raise SonarrSecretsUnauthorizedError(
                f"Unable to find Sonarr version in system status metadata: {system_status}",
            ) from None
        except TypeError as err:
            raise SonarrSecretsUnauthorizedError(
                (
                    f"Unable to parse Sonarr system status metadata: {err} "
                    f"(metadata object: {system_status})"
                ),
            ) from None
        return cls(
            hostname=cast(NonEmptyStr, hostname),
            port=cast(Port, port),
            protocol=cast(SonarrProtocol, protocol),
            url_base=_url_base,
            api_key=cast(SonarrApiKey, api_key),
            version=version,
        )

    def test(self) -> bool:
        # We already perform API requests as part of instantiating the secrets object.
        # If the object exists, then the connection test is already successful.
        return True
