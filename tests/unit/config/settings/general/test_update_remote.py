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
Test the `update_remote` method on the General Settings configuration model.
"""

from __future__ import annotations

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
    Check that if the local and remote instance configuration are identical,
    no changes are pushed to the remote instance, and the method reports that
    the configuration is up to date.
    """

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)

    # The local configuration is created this way to make Pydantic
    # register all of the values as "set", and therefore Buildarr
    # will consider them "managed" when looking for changes.
    assert not GeneralSettings(**GeneralSettings().model_dump()).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


@pytest.mark.parametrize("attr_value", ["*", "127.0.0.1"])
def test_host_bind_address(sonarr_api, attr_value) -> None:
    """
    Check that the `host.bind_address` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "bindAddress": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"bind_address": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(host={"bind_address": "192.0.2.1"}),  # type: ignore[arg-type]
    )


def test_host_port(sonarr_api) -> None:
    """
    Check that the `host.port` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 8990

    api_host_config = {**HOST_CONFIG_DEFAULTS, "port": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"port": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


def test_host_ssl_port(sonarr_api) -> None:
    """
    Check that the `host.ssl_port` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 9889

    api_host_config = {**HOST_CONFIG_DEFAULTS, "sslPort": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"ssl_port": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_host_use_ssl(sonarr_api, attr_value) -> None:
    """
    Check that the `host.use_ssl` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "enableSsl": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "enableSsl": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"use_ssl": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            host={"use_ssl": not attr_value},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", [None, "", "/sonarr"])
def test_host_url_base(sonarr_api, attr_value) -> None:
    """
    Check that the `host.url_base` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "urlBase": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "urlBase": "" if attr_value else "/sonarr"})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"url_base": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            host={"url_base": None if attr_value else "/sonarr"},  # type: ignore[arg-type]
        ),
    )


def test_host_instance_name(sonarr_api) -> None:
    """
    Check that the `host.instance_name` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "Sonarr (Managed by Buildarr)"

    api_host_config = {**HOST_CONFIG_DEFAULTS, "instanceName": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        host={"instance_name": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


def test_security_authentication_none(sonarr_api) -> None:
    """
    Check that the `security.authentication` attribute, when set to `none`,
    is updated when the local configuration attribute is different to the remote instance.
    """

    api_host_config = {
        **HOST_CONFIG_DEFAULTS,
        "authenticationMethod": "none",
        "username": "test",
        "password": "test",
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "authenticationMethod": "forms",
            "username": "test",
            "password": "test",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        security={"authentication": AuthenticationMethod.none},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            security={  # type: ignore[arg-type]
                "authentication": AuthenticationMethod.form,
                "username": "test",
                "password": "test",
            },
        ),
    )


@pytest.mark.parametrize("attr_value", ["basic", "forms"])
def test_security_authentication_enabled(sonarr_api, attr_value) -> None:
    """
    Check that the `security.authentication` attribute, when enabled,
    is updated when the local configuration attribute is different to the remote instance.
    """

    api_host_config = {
        **HOST_CONFIG_DEFAULTS,
        "authenticationMethod": attr_value,
        "username": "test",
        "password": "test",
    }

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        security={  # type: ignore[arg-type]
            "authentication": AuthenticationMethod(attr_value),
            "username": "test",
            "password": "test",
        },
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_security_username(sonarr_api, attr_value) -> None:
    """
    Check that the `security.username` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "username": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "username": "" if attr_value else "test"})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        security={"username": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            security={"username": None if attr_value else "test"},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_security_password(sonarr_api, attr_value) -> None:
    """
    Check that the `security.password` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "password": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "password": "" if attr_value else "test"})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        security={"password": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            security={"password": None if attr_value else "test"},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", ["enabled", "disabledForLocalAddresses", "disabled"])
def test_security_certificate_validation(sonarr_api, attr_value) -> None:
    """
    Check that the `security.certificate_validation` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "certificateValidation": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "certificateValidation": "enabled" if attr_value == "disabled" else "disabled",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        security={  # type: ignore[arg-type]
            "certificate_validation": CertificateValidation(attr_value),
        },
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            security={  # type: ignore[arg-type]
                "certificate_validation": (
                    CertificateValidation.enabled
                    if attr_value == "disabled"
                    else CertificateValidation.disabled
                ),
            },
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_proxy_enable(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.enable` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "proxyEnabled": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyEnabled": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        proxy={"enable": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            proxy={"enable": not attr_value},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", ["http", "socks4", "socks5"])
def test_proxy_proxy_type(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.proxy_type` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "proxyType": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "proxyType": "socks5" if attr_value == "http" else "http",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        proxy={"proxy_type": ProxyType(attr_value)},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            proxy={  # type: ignore[arg-type]
                "proxy_type": ProxyType.socks5 if attr_value == "http" else ProxyType.http,
            },
        ),
    )


@pytest.mark.parametrize("attr_value", [[], ["127.0.0.1"], ["*"]])
def test_proxy_ignored_addresses(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.ignored_addresses` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "proxyBypassFilter": ",".join(attr_value)}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "proxyBypassFilter": "" if attr_value else "*",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        proxy={"ignored_addresses": set(attr_value)},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            proxy={  # type: ignore[arg-type]
                "ignored_addresses": set() if attr_value else {"*"},
            },
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_proxy_bypass_proxy_for_local_addresses(sonarr_api, attr_value) -> None:
    """
    Check that the `proxy.bypass_proxy_for_local_addresses` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "proxyBypassLocalAddresses": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "proxyBypassLocalAddresses": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        proxy={"bypass_proxy_for_local_addresses": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            proxy={"bypass_proxy_for_local_addresses": not attr_value},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", ["info", "debug", "trace"])
def test_logging_log_level(sonarr_api, attr_value) -> None:
    """
    Check that the `logging.log_level` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "logLevel": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "logLevel": "debug" if attr_value == "info" else "info",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        logging={"log_level": SonarrLogLevel(attr_value)},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            logging={  # type: ignore[arg-type]
                "log_level": SonarrLogLevel.DEBUG if attr_value == "info" else SonarrLogLevel.INFO,
            },
        ),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_analytics_send_anonymous_usage_data(sonarr_api, attr_value) -> None:
    """
    Check that the `analytics.send_anonymous_usage_data` attribute
    is being populated by its API value.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "analyticsEnabled": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "analyticsEnabled": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        analytics={"send_anonymous_usage_data": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            analytics={"send_anonymous_usage_data": not attr_value},  # type: ignore[arg-type]
        ),
    )


def test_updates_branch(sonarr_api) -> None:
    """
    Check that the `updates.branch` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "develop"

    api_host_config = {**HOST_CONFIG_DEFAULTS, "branch": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        updates={"branch": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


@pytest.mark.parametrize("attr_value", [False, True])
def test_updates_automatic(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.automatic` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "updateAutomatically": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "updateAutomatically": not attr_value})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        updates={"automatic": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            updates={"automatic": not attr_value},  # type: ignore[arg-type]
        ),
    )


@pytest.mark.parametrize("attr_value", ["builtIn", "script", "external", "apt", "docker"])
def test_updates_mechanism(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.mechanism` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "updateMechanism": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(
        {
            **HOST_CONFIG_DEFAULTS,
            "updateMechanism": "external" if attr_value == "docker" else "docker",
        },
    )
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        updates={"mechanism": UpdateMechanism(attr_value)},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            updates={  # type: ignore[arg-type]
                "mechanism": (
                    UpdateMechanism.external if attr_value == "docker" else UpdateMechanism.docker
                ),
            },
        ),
    )


@pytest.mark.parametrize("attr_value", [None, "", "test"])
def test_updates_script_path(sonarr_api, attr_value) -> None:
    """
    Check that the `updates.script_path` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    api_host_config = {**HOST_CONFIG_DEFAULTS, "updateScriptPath": attr_value or ""}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json({**HOST_CONFIG_DEFAULTS, "updateScriptPath": "" if attr_value else "test"})
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        updates={"script_path": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(
            updates={"script_path": None if attr_value else "test"},  # type: ignore[arg-type]
        ),
    )


def test_backup_folder(sonarr_api) -> None:
    """
    Check that the `backup.folder` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = "backup-dir"

    api_host_config = {**HOST_CONFIG_DEFAULTS, "backupFolder": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        backup={"folder": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


def test_backup_interval(sonarr_api) -> None:
    """
    Check that the `backup.interval` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 1

    api_host_config = {**HOST_CONFIG_DEFAULTS, "backupInterval": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        backup={"interval": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )


def test_backup_retention(sonarr_api) -> None:
    """
    Check that the `backup.retention` attribute is updated when the
    local configuration attribute is different to the remote instance.
    """

    attr_value = 14

    api_host_config = {**HOST_CONFIG_DEFAULTS, "backupRetention": attr_value}

    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host",
        method="GET",
    ).respond_with_json(HOST_CONFIG_DEFAULTS)
    sonarr_api.server.expect_ordered_request(
        "/api/v3/config/host/0",
        method="PUT",
        json=api_host_config,
    ).respond_with_json(api_host_config, status=202)

    assert GeneralSettings(
        backup={"retention": attr_value},  # type: ignore[arg-type]
    ).update_remote(
        tree="sonarr.settings.general",
        secrets=sonarr_api.secrets,
        remote=GeneralSettings(),
    )
