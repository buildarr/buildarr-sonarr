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
Sonarr plugin API functions.
"""

from __future__ import annotations

import re

from http import HTTPStatus
from logging import getLogger
from typing import TYPE_CHECKING

import json5  # type: ignore[import]
import requests

from buildarr.state import state

from .exceptions import SonarrAPIError

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Union

    from .secrets import SonarrSecrets


logger = getLogger(__name__)

INITIALIZE_JS_RES_PATTERN = re.compile(r"(?s)^window\.Sonarr = ({.*});$")


def get_initialize_js(host_url: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the Sonarr session initialisation metadata, including the API key.

    Args:
        host_url (str): Sonarr instance URL.
        api_key (str): Sonarr instance API key, if required. Defaults to `None`.

    Returns:
        Session initialisation metadata
    """

    url = f"{host_url}/initialize.js"

    logger.debug("GET %s", url)

    res = requests.get(
        url,
        headers={"X-Api-Key": api_key} if api_key else None,
        timeout=state.request_timeout,
        allow_redirects=False,
    )

    if res.status_code != HTTPStatus.OK:
        logger.debug("GET %s -> status_code=%i res=%s", url, res.status_code, res.text)
        if res.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FOUND):
            status_code: int = HTTPStatus.UNAUTHORIZED
            error_message = "Unauthorized"
        else:
            status_code = res.status_code
            error_message = f"Unexpected response with error code {res.status_code}: {res.text}"
        raise SonarrAPIError(
            f"Unable to retrieve '{url}': {error_message}",
            status_code=status_code,
        )

    res_match = re.match(INITIALIZE_JS_RES_PATTERN, res.text)
    if not res_match:
        raise SonarrAPIError(
            f"No matches for 'initialize.js' parsing: {res.text}",
            status_code=res.status_code,
        )
    res_json = json5.loads(res_match.group(1))

    logger.debug("GET %s -> status_code=%i res=%s", url, res.status_code, repr(res_json))

    return res_json


def api_get(
    secrets: Union[SonarrSecrets, str],
    api_url: str,
    *,
    api_key: Optional[str] = None,
    use_api_key: bool = True,
    expected_status_code: HTTPStatus = HTTPStatus.OK,
    session: Optional[requests.Session] = None,
) -> Any:
    """
    Send an API `GET` request.

    Args:
        secrets (Union[SonarrSecrets, str]): Secrets metadata, or host URL.
        api_url (str): API command.
        expected_status_code (HTTPStatus): Expected response status. Defaults to `200 OK`.

    Returns:
        Response object
    """

    if isinstance(secrets, str):
        host_url = secrets
        host_api_key = api_key
    else:
        host_url = secrets.host_url
        host_api_key = secrets.api_key.get_secret_value()

    if not use_api_key:
        host_api_key = None

    url = f"{host_url}/{api_url.lstrip('/')}"

    logger.debug("GET %s", url)

    if not session:
        session = requests.Session()
    res = session.get(
        url,
        headers={"X-Api-Key": host_api_key} if host_api_key else None,
        timeout=state.request_timeout,
    )
    try:
        res_json = res.json()
    except requests.JSONDecodeError:
        api_error(method="GET", url=url, response=res)

    logger.debug("GET %s -> status_code=%i res=%s", url, res.status_code, repr(res_json))

    if res.status_code != expected_status_code:
        api_error(method="GET", url=url, response=res)

    return res_json


def api_post(
    secrets: Union[SonarrSecrets, str],
    api_url: str,
    req: Any = None,
    session: Optional[requests.Session] = None,
    use_api_key: bool = True,
    expected_status_code: HTTPStatus = HTTPStatus.CREATED,
) -> Any:
    """
    Send a `POST` request to a Sonarr instance.

    Args:
        secrets (Union[SonarrSecrets, str]): Sonarr secrets metadata, or host URL.
        api_url (str): Sonarr API command.
        req (Any): Request (JSON-serialisable).
        expected_status_code (HTTPStatus): Expected response status. Defaults to `201 Created`.

    Returns:
        Response object
    """

    if isinstance(secrets, str):
        host_url = secrets
        api_key = None
    else:
        host_url = secrets.host_url
        api_key = secrets.api_key.get_secret_value() if use_api_key else None
    url = f"{host_url}/{api_url.lstrip('/')}"

    logger.debug("POST %s <- req=%s", url, repr(req))

    if not session:
        session = requests.Session()
    res = session.post(
        url,
        headers={"X-Api-Key": api_key} if api_key else None,
        timeout=state.request_timeout,
        **({"json": req} if req is not None else {}),
    )
    try:
        res_json = res.json()
    except requests.JSONDecodeError:
        api_error(method="POST", url=url, response=res)

    logger.debug("POST %s -> status_code=%i res=%s", url, res.status_code, repr(res_json))

    if res.status_code != expected_status_code:
        api_error(method="POST", url=url, response=res)

    return res_json


def api_put(
    secrets: Union[SonarrSecrets, str],
    api_url: str,
    req: Any,
    session: Optional[requests.Session] = None,
    use_api_key: bool = True,
    expected_status_code: HTTPStatus = HTTPStatus.ACCEPTED,
) -> Any:
    """
    Send a `PUT` request to a Sonarr instance.

    Args:
        secrets (Union[SonarrSecrets, str]): Sonarr secrets metadata, or host URL.
        api_url (str): Sonarr API command.
        req (Any): Request (JSON-serialisable).
        expected_status_code (HTTPStatus): Expected response status. Defaults to `200 OK`.

    Returns:
        Response object
    """

    if isinstance(secrets, str):
        host_url = secrets
        api_key = None
    else:
        host_url = secrets.host_url
        api_key = secrets.api_key.get_secret_value() if use_api_key else None
    url = f"{host_url}/{api_url.lstrip('/')}"

    logger.debug("PUT %s <- req=%s", url, repr(req))

    if not session:
        session = requests.Session()
    res = session.put(
        url,
        headers={"X-Api-Key": api_key} if api_key else None,
        json=req,
        timeout=state.request_timeout,
    )
    try:
        res_json = res.json()
    except requests.JSONDecodeError:
        api_error(method="PUT", url=url, response=res)

    logger.debug("PUT %s -> status_code=%i res=%s", url, res.status_code, repr(res_json))

    if res.status_code != expected_status_code:
        api_error(method="PUT", url=url, response=res)

    return res_json


def api_delete(
    secrets: Union[SonarrSecrets, str],
    api_url: str,
    session: Optional[requests.Session] = None,
    use_api_key: bool = True,
    expected_status_code: HTTPStatus = HTTPStatus.OK,
) -> None:
    """
    Send a `DELETE` request to a Sonarr instance.

    Args:
        secrets (Union[SonarrSecrets, str]): Sonarr secrets metadata, or host URL.
        api_url (str): Sonarr API command.
        expected_status_code (HTTPStatus): Expected response status. Defaults to `200 OK`.
    """

    if isinstance(secrets, str):
        host_url = secrets
        api_key = None
    else:
        host_url = secrets.host_url
        api_key = secrets.api_key.get_secret_value() if use_api_key else None
    url = f"{host_url}/{api_url.lstrip('/')}"

    logger.debug("DELETE %s", url)

    if not session:
        session = requests.Session()
    res = session.delete(
        url,
        headers={"X-Api-Key": api_key} if api_key else None,
        timeout=state.request_timeout,
    )

    logger.debug("DELETE %s -> status_code=%i", url, res.status_code)

    if res.status_code != expected_status_code:
        api_error(method="DELETE", url=url, response=res, parse_response=False)


def api_error(
    method: str,
    url: str,
    response: requests.Response,
    parse_response: bool = True,
) -> None:
    """
    Process an error response from the Sonarr API.

    Args:
        method (str): HTTP method.
        url (str): API command URL.
        response (requests.Response): Response metadata.
        parse_response (bool, optional): Parse response error JSON. Defaults to True.

    Raises:
        Sonarr API exception
    """

    error_message = (
        f"Unexpected response with status code {response.status_code} from '{method} {url}':"
    )
    if parse_response:
        res_json = response.json()
        try:
            error_message += f" {_api_error(res_json)}"
        except TypeError:
            for error in res_json:
                error_message += f"\n{_api_error(error)}"
        except KeyError:
            error_message += f" {res_json}"
    raise SonarrAPIError(error_message, status_code=response.status_code) from None


def _api_error(res_json: Any) -> str:
    """
    Generate an error message from a response object.

    Args:
        res_json (Any): Response object

    Returns:
        String containing one or more error messages
    """

    try:
        try:
            error_message = f"{res_json['propertyName']}: {res_json['errorMessage']}"
            try:
                error_message += f" (attempted value: {res_json['attemptedValue']})"
            except KeyError:
                pass
            return error_message
        except KeyError:
            pass
        try:
            return f"{res_json['message']}\n{res_json['description']}"
        except KeyError:
            pass
        try:
            return res_json["error"]
        except KeyError:
            pass
        return res_json["message"]
    except KeyError:
        return f"(Unsupported error JSON format) {res_json}"
