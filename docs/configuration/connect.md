# Connect

Sonarr supports configuring connections to external applications and services.

These are not only for Sonarr to communicate with the outside world, they can also be useful for monitoring
since the user can be alerted by a variety of possible service when some kind of event (or problem)
occurs in Sonarr.

## Configuring connections

##### ::: buildarr_sonarr.config.connect.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_series_delete
        - on_episode_file_delete
        - on_episode_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_application_update

## Boxcar

##### ::: buildarr_sonarr.config.connect.BoxcarConnection
    options:
      members:
        - type
        - access_token

## Custom Script

##### ::: buildarr_sonarr.config.connect.CustomscriptConnection
    options:
      members:
        - type
        - path

## Discord

##### ::: buildarr_sonarr.config.connect.DiscordConnection
    options:
      members:
        - type
        - webhook_url
        - username
        - avatar
        - host
        - on_grab_fields
        - on_import_fields

## Email

##### ::: buildarr_sonarr.config.connect.EmailConnection
    options:
      members:
        - type
        - server
        - port
        - use_encryption
        - username
        - password
        - from_address
        - recipient_addresses
        - cc_addresses
        - bcc_addresses

## Emby

##### ::: buildarr_sonarr.config.connect.EmbyConnection
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - api_key
        - send_notifications
        - update_library

## Gotify

##### ::: buildarr_sonarr.config.connect.GotifyConnection
    options:
      members:
        - type
        - server
        - app_token
        - priority

## Join

##### ::: buildarr_sonarr.config.connect.JoinConnection
    options:
      members:
        - type
        - api_key
        - device_names
        - priority

## Kodi (XBMC)

##### ::: buildarr_sonarr.config.connect.KodiConnection
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - gui_notification
        - display_time
        - update_library
        - clean_library
        - always_update

## Mailgun

##### ::: buildarr_sonarr.config.connect.MailgunConnection
    options:
      members:
        - type
        - api_key
        - use_eu_endpoint
        - from_address
        - sender_domain
        - recipient_addresses

## Plex Home Theater

##### ::: buildarr_sonarr.config.connect.PlexHomeTheaterConnection
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - gui_notification
        - display_time
        - update_library
        - clean_library
        - always_update

## Plex Media Center

##### ::: buildarr_sonarr.config.connect.PlexMediaCenterConnection
    options:
      members:
        - type
        - host
        - port
        - username
        - password

## Plex Media Server

##### ::: buildarr_sonarr.config.connect.PlexMediaServerConnection
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - auth_token
        - update_library

## Prowl

##### ::: buildarr_sonarr.config.connect.ProwlConnection
    options:
      members:
        - type
        - api_key
        - priority

## Pushbullet

##### ::: buildarr_sonarr.config.connect.PushbulletConnection
    options:
      members:
        - type
        - api_key
        - device_ids
        - channel_tags
        - sender_id

## Pushover

##### ::: buildarr_sonarr.config.connect.PushoverConnection
    options:
      members:
        - type
        - user_key
        - api_key
        - devices
        - priority
        - retry
        - expire
        - sound

## SendGrid

##### ::: buildarr_sonarr.config.connect.SendgridConnection
    options:
      members:
        - type
        - api_key
        - from_address
        - recipient_addresses

## Slack

##### ::: buildarr_sonarr.config.connect.SlackConnection
    options:
      members:
        - type
        - webhook_url
        - username
        - icon
        - channel

## Synology Indexer

##### ::: buildarr_sonarr.config.connect.SynologyIndexerConnection
    options:
      members:
        - type
        - update_library

## Telegram

##### ::: buildarr_sonarr.config.connect.TelegramConnection
    options:
      members:
        - type
        - bot_token
        - chat_id
        - send_silently

## Trakt

##### ::: buildarr_sonarr.config.connect.TraktConnection
    options:
      members:
        - type
        - access_token
        - refresh_token
        - expires
        - auth_user

## Twitter

##### ::: buildarr_sonarr.config.connect.TwitterConnection
    options:
      members:
        - type
        - consumer_key
        - consumer_secret
        - access_token
        - access_token_secret
        - mention
        - direct_message

## Webhook

##### ::: buildarr_sonarr.config.connect.WebhookConnection
    options:
      members:
        - type
        - webhook_url
        - method
        - username
        - password
