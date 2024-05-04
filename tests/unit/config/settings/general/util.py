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
General Settings unit test constants and utility functions.
"""

from __future__ import annotations

HOST_CONFIG_DEFAULTS = {
    # Uses default values set in the model,
    # which may be different to the real defaults.
    # In this case, the model defaults are not used.
    "id": 0,
    # Host
    "bindAddress": "*",
    "port": 8989,
    "sslPort": 9898,
    "enableSsl": False,
    "urlBase": "",
    "instanceName": "Sonarr",
    # Security
    "authenticationMethod": "none",
    "username": "",
    "password": "",
    "certificateValidation": "enabled",
    # Proxy
    "proxyEnabled": False,
    "proxyType": "http",
    "proxyHostname": "",
    "proxyPort": 8080,
    "proxyUsername": "",
    "proxyPassword": "",
    "proxyBypassFilter": "",
    "proxyBypassLocalAddresses": True,
    # Logging
    "logLevel": "info",
    # Analytics
    "analyticsEnabled": True,
    # Updates
    "branch": "main",
    "updateAutomatically": False,
    "updateMechanism": "docker",
    "updateScriptPath": "",
    # Backup
    "backupFolder": "Backups",
    "backupInterval": 7,  # days
    "backupRetention": 28,  # days
}
