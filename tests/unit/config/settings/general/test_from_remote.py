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
Test the `from_remote` class method on the General Settings configuration model.
"""

from __future__ import annotations

from ipaddress import ip_address

import pytest

from buildarr_sonarr.config.general import (
    AuthenticationMethod,
    CertificateValidation,
    ProxyType,
    SonarrGeneralSettingsConfig as GeneralSettings,
    SonarrLogLevel,
    UpdateMechanism,
)

from .util import HOST_CONFIG_DEFAULTS


def test_defaults(sonarr_api) -> None:
    """
    Check that providing the default values results in a model object
    that is equal to one created directly.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)

    assert GeneralSettings.from_remote(sonarr_api.secrets) == GeneralSettings()


@pytest.mark.parametrize("attr_value", ["*", "127.0.0.1"])
def test_host_bind_address(sonarr_api, attr_value) -> None:
    """
    Check that the `host.bind_address` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "bindAddress": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.bind_address == (
        ip_address(attr_value) if attr_value != "*" else attr_value
    )


def test_host_port(sonarr_api) -> None:
    """
    Check that the `host.port` attribute is being populated by its API value.
    """

    attr_value = 8990

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "port": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.port == attr_value


def test_host_ssl_port(sonarr_api) -> None:
    """
    Check that the `host.ssl_port` attribute is being populated by its API value.
    """

    attr_value = 9889

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "sslPort": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.ssl_port == attr_value


@pytest.mark.parametrize("attr_value", [False, True])
def test_host_use_ssl(sonarr_api, attr_value) -> None:
    """
    Check that the `host.use_ssl` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "enableSsl": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.use_ssl is attr_value


@pytest.mark.parametrize("attr_value", [None, "", "/sonarr"])
def test_host_url_base(sonarr_api, attr_value) -> None:
    """
    Check that the `host.url_base` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "urlBase": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.url_base == (attr_value or None)


def test_host_instance_name(sonarr_api) -> None:
    """
    Check that the `host.instance_name` attribute is being populated by its API value.
    """

    attr_value = "Sonarr (Managed by Buildarr)"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "instanceName": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).host.instance_name == attr_value


def test_security_authentication_none(sonarr_api) -> None:
    """
    Check that the `security.authentication` attribute is being populated by its API value
    when set to `none`.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "authenticationMethod": "none"})

    assert (
        GeneralSettings.from_remote(sonarr_api.secrets).security.authentication
        == AuthenticationMethod.none
    )


@pytest.mark.parametrize("attr_value", ["basic", "forms"])
def test_security_authentication_enabled(sonarr_api, attr_value) -> None:
    """
    Check that the `security.authentication_method` attribute is being populated by its API value
    when set to an "enabled" value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "authenticationMethod": attr_value,
            "username": "test",
            "password": "test",
        },
    )

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).security.authentication == AuthenticationMethod(attr_value)


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_security_username(sonarr_api, attr_value) -> None:
    """
    Check that the `security.username` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "username": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).security.username == (attr_value or None)


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_security_password(sonarr_api, attr_value) -> None:
    """
    Check that the `security.password` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "password": attr_value})

    password = GeneralSettings.from_remote(sonarr_api.secrets).security.password

    assert (
        (password.get_secret_value() == attr_value)  # type: ignore[union-attr]
        if attr_value
        else password is None
    )


@pytest.mark.parametrize("attr_value", ["enabled", "disabledForLocalAddresses", "disabled"])
def test_security_certificate_validation(sonarr_api, attr_value) -> None:
    """
    Check that the `security.certificate_validation` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "certificateValidation": attr_value})

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).security.certificate_validation == CertificateValidation(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_proxy_enable(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.enable` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyEnabled": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).proxy.enable is attr_value


@pytest.mark.parametrize("attr_value", ["http", "socks4", "socks5"])
def test_proxy_proxy_type(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.proxy_type` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyType": attr_value})

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).proxy.proxy_type == ProxyType(attr_value)


@pytest.mark.parametrize("attr_value", [[], ["127.0.0.1"], ["*"]])
def test_proxy_ignored_addresses(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.ignored_addresses` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyBypassFilter": ",".join(attr_value)})

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).proxy.ignored_addresses == set(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_proxy_bypass_proxy_for_local_addresses(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.bypass_proxy_for_local_addresses` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyBypassLocalAddresses": attr_value})

    assert (
        GeneralSettings.from_remote(
            sonarr_api.secrets,
        ).proxy.bypass_proxy_for_local_addresses
        is attr_value
    )


@pytest.mark.parametrize("attr_value", ["info", "debug", "trace"])
def test_logging_log_level(sonarr_api, attr_value) -> None:
    """
    Check that the `logging.log_level` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "logLevel": attr_value})

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).logging.log_level == SonarrLogLevel(attr_value)


@pytest.mark.parametrize("attr_value", [False, True])
def test_analytics_send_anonymous_usage_data(sonarr_api, attr_value) -> None:
    """
    Check that the `analytics.send_anonymous_usage_data` attribute
    is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "analyticsEnabled": attr_value})

    assert (
        GeneralSettings.from_remote(
            sonarr_api.secrets,
        ).analytics.send_anonymous_usage_data
        is attr_value
    )


def test_updates_branch(sonarr_api) -> None:
    """
    Check that the `updates.branch` attribute is being populated by its API value.
    """

    attr_value = "develop"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "branch": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).updates.branch == attr_value


@pytest.mark.parametrize("attr_value", [False, True])
def test_updates_automatic(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.automatic` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "updateAutomatically": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).updates.automatic is attr_value


@pytest.mark.parametrize("attr_value", ["builtIn", "script", "external", "apt", "docker"])
def test_updates_mechanism(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.mechanism` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "updateMechanism": attr_value})

    assert GeneralSettings.from_remote(
        sonarr_api.secrets,
    ).updates.mechanism == UpdateMechanism(attr_value)


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_updates_script_path(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.script_path` attribute is being populated by its API value.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "updateScriptPath": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).updates.script_path == (
        attr_value or None
    )


def test_backup_folder(sonarr_api) -> None:
    """
    Check that the `backup.folder` attribute is being populated by its API value.
    """

    attr_value = "backup-dir"

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "backupFolder": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).backup.folder == attr_value


def test_backup_interval(sonarr_api) -> None:
    """
    Check that the `backup.interval` attribute is being populated by its API value.
    """

    attr_value = 1

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "backupInterval": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).backup.interval == attr_value


def test_backup_retention(sonarr_api) -> None:
    """
    Check that the `backup.retention` attribute is being populated by its API value.
    """

    attr_value = 14

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "backupRetention": attr_value})

    assert GeneralSettings.from_remote(sonarr_api.secrets).backup.retention == attr_value
