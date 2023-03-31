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
      show_root_heading: false
      show_source: false

## Configuring indexers

##### ::: buildarr_sonarr.config.indexers.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - anime_standard_format_search
        - indexer_priority
        - download_client
        - tags
      show_root_heading: false
      show_source: false

## Fanzub

##### ::: buildarr_sonarr.config.indexers.FanzubIndexer
    options:
      members:
        - type
        - rss_url
      show_root_heading: false
      show_source: false

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
        - additional_parameters
      show_root_heading: false
      show_source: false

## OmgWtfNZBs

##### ::: buildarr_sonarr.config.indexers.OmgwtfnzbsIndexer
    options:
      members:
        - type
        - username
        - api_key
        - delay
      show_root_heading: false
      show_source: false

## Torrent Indexers

##### ::: buildarr_sonarr.config.indexers.TorrentIndexer
    options:
      members:
        - minimum_seeders
        - seed_ratio
        - seed_time
        - seasonpack_seed_time
      show_root_heading: false
      show_source: false

## BroadcasTheNet

##### ::: buildarr_sonarr.config.indexers.BroadcasthenetIndexer
    options:
      members:
        - type
        - api_url
        - api_key
      show_root_heading: false
      show_source: false

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
      show_root_heading: false
      show_source: false

## HDBits

##### ::: buildarr_sonarr.config.indexers.HdbitsIndexer
    options:
      members:
        - type
        - username
        - api_key
        - api_url
      show_root_heading: false
      show_source: false

## IP Torrents

##### ::: buildarr_sonarr.config.indexers.IptorrentsIndexer
    options:
      members:
        - type
        - feed_url
      show_root_heading: false
      show_source: false

## Nyaa

##### ::: buildarr_sonarr.config.indexers.NyaaIndexer
    options:
      members:
        - type
        - website_url
        - additional_parameters
      show_root_heading: false
      show_source: false

## Rarbg

##### ::: buildarr_sonarr.config.indexers.RarbgIndexer
    options:
      members:
        - type
        - api_url
        - ranked_only
        - captcha_token
      show_root_heading: false
      show_source: false

## Torrent RSS Feed

##### ::: buildarr_sonarr.config.indexers.TorrentrssfeedIndexer
    options:
      members:
        - type
        - full_rss_feed_url
        - cookie
        - allow_zero_size
      show_root_heading: false
      show_source: false

## TorrentLeech

##### ::: buildarr_sonarr.config.indexers.TorrentleechIndexer
    options:
      members:
        - type
        - website_url
        - api_key
      show_root_heading: false
      show_source: false

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
        - additional_parameters
      show_root_heading: false
      show_source: false
