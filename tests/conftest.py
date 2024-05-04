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
Unit test fixtures.
"""

from __future__ import annotations

import random
import string

from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import pytest

from buildarr_sonarr.secrets import SonarrSecrets

if TYPE_CHECKING:
    from typing import Callable, Optional

    from pytest_httpserver import HTTPServer


@dataclass(frozen=True)
class SonarrAPI:
    server: HTTPServer
    secrets: SonarrSecrets


@pytest.fixture
def api_key() -> str:
    """
    Fixture for generating a random *Arr-compatible API key.

    Returns:
        str: API key
    """

    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=32),  # noqa: S311
    )


@pytest.fixture
def sonarr_api_factory(httpserver: HTTPServer, api_key) -> Callable[..., SonarrAPI]:
    """
    A factory fixture for starting up a stub Sonarr API for tests,
    where the expected inputs and outputs can be defined and validated.

    Returns:
        Callable[..., SonarrAPI]: The factory function.
    """

    def _sonarr_api_factory(url_base: Optional[str] = None, version: str = "3.0.10.1567"):
        return SonarrAPI(
            server=httpserver,
            secrets=SonarrSecrets(
                hostname="localhost",  # type: ignore[arg-type]
                port=urlparse(httpserver.url_for("")).port,
                protocol="http",
                url_base=url_base,
                api_key=api_key,
                version=version,  # type: ignore[arg-type]
            ),
        )

    return _sonarr_api_factory


@pytest.fixture
def sonarr_api(sonarr_api_factory) -> SonarrAPI:
    """
    Fixture for creating a stub Sonarr API with the default options set.

    For more information, refer to the docstring for `sonarr_api_factory`.

    Returns:
        SonarrAPI: The Sonarr API object.
    """

    return sonarr_api_factory()
