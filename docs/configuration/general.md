# General

General configuration for Sonarr are separated by category.

```yaml
sonarr:
  settings:
    general:
      host:
        bind_address: "*"
        port: 8989
        url_base: null
        instance_name: "Sonarr (Example)"
      security:
        authentication: "none"
      proxy:
        enable: false
      logging:
        log_level: "INFO"
      analytics:
        send_anonymous_usage_data: false
      updates:
        branch: "main"
        automatic: false
        mechanism: "docker"
      backup:
        folder: "Backups"
        interval: 7
        retention: 28
```

Some of the settings may affect Buildarr's ability to connect with the Sonarr instance.
Take care when changing these settings.

## Host

##### ::: buildarr_sonarr.config.general.HostGeneralSettings
    options:
      members:
        - bind_address
        - port
        - ssl_port
        - use_ssl
        - url_base
        - instance_name

## Security

##### ::: buildarr_sonarr.config.general.SecurityGeneralSettings
    options:
      members:
        - authentication
        - username
        - password
        - certificate_validation

## Proxy

##### ::: buildarr_sonarr.config.general.ProxyGeneralSettings
    options:
      members:
        - enable
        - proxy_type
        - hostname
        - port
        - username
        - password
        - ignored_addresses
        - bypass_proxy_for_local_addresses

## Logging

##### ::: buildarr_sonarr.config.general.LoggingGeneralSettings
    options:
      members:
        - log_level

## Analytics

##### ::: buildarr_sonarr.config.general.AnalyticsGeneralSettings
    options:
      members:
        - send_anonymous_usage_data

## Updates

##### ::: buildarr_sonarr.config.general.UpdatesGeneralSettings
    options:
      members:
        - branch
        - automatic
        - mechanism
        - script_path

## Backup

##### ::: buildarr_sonarr.config.general.BackupGeneralSettings
    options:
      members:
        - folder
        - interval
        - retention
