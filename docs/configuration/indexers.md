# Indexers

##### ::: buildarr_sonarr.config.indexers.SonarrIndexersSettingsConfig
    options:
      members:
        - minimum_age
        - retention
        - maximum_size
        - rss_sync_interval
        - delete_unmanaged
        - definitions

## Configuring indexers

##### ::: buildarr_sonarr.config.indexers.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client
        - tags

## Fanzub

##### ::: buildarr_sonarr.config.indexers.FanzubIndexer
    options:
      members:
        - type
        - rss_url
        - anime_standard_format_search

## Newznab

##### ::: buildarr_sonarr.config.indexers.NewznabIndexer
    options:
      members:
        - type
        - url
        - api_path
        - password
        - categories
        - anime_categories
        - anime_standard_format_search
        - additional_parameters

## OmgWtfNZBs

##### ::: buildarr_sonarr.config.indexers.OmgwtfnzbsIndexer
    options:
      members:
        - type
        - username
        - api_key
        - delay

## Torrent Indexers

##### ::: buildarr_sonarr.config.indexers.TorrentIndexer
    options:
      members:
        - minimum_seeders
        - seed_ratio
        - seed_time
        - seasonpack_seed_time

## BroadcasTheNet

##### ::: buildarr_sonarr.config.indexers.BroadcasthenetIndexer
    options:
      members:
        - type
        - api_url
        - api_key

## Filelist

##### ::: buildarr_sonarr.config.indexers.FilelistIndexer
    options:
      members:
        - type
        - username
        - passkey
        - api_url
        - categories
        - anime_categories

## HDBits

##### ::: buildarr_sonarr.config.indexers.HdbitsIndexer
    options:
      members:
        - type
        - username
        - api_key
        - api_url

## IP Torrents

##### ::: buildarr_sonarr.config.indexers.IptorrentsIndexer
    options:
      members:
        - type
        - feed_url

## Nyaa

##### ::: buildarr_sonarr.config.indexers.NyaaIndexer
    options:
      members:
        - type
        - website_url
        - anime_standard_format_search
        - additional_parameters

## Rarbg

##### ::: buildarr_sonarr.config.indexers.RarbgIndexer
    options:
      members:
        - type
        - api_url
        - ranked_only
        - captcha_token

## Torrent RSS Feed

##### ::: buildarr_sonarr.config.indexers.TorrentrssfeedIndexer
    options:
      members:
        - type
        - full_rss_feed_url
        - cookie
        - allow_zero_size

## TorrentLeech

##### ::: buildarr_sonarr.config.indexers.TorrentleechIndexer
    options:
      members:
        - type
        - website_url
        - api_key

## Torznab

##### ::: buildarr_sonarr.config.indexers.TorznabIndexer
    options:
      members:
        - type
        - url
        - api_path
        - password
        - categories
        - anime_categories
        - anime_standard_format_search
        - additional_parameters
