# Import Lists

##### ::: buildarr_sonarr.config.import_lists.SonarrImportListsSettingsConfig
    options:
      members:
        - delete_unmanaged
        - delete_unmanaged_exclusions
        - definitions
        - exclusions

## Configuring import lists

The following

##### ::: buildarr_sonarr.config.import_lists.ImportList
    options:
      members:
        - enable_automatic_add
        - monitor
        - root_folder
        - quality_profile
        - language_profile
        - series_type
        - season_folder
        - tags

## Sonarr

##### ::: buildarr_sonarr.config.import_lists.SonarrImportList
    options:
      members:
        - type
        - instance_name
        - full_url
        - api_key
        - source_quality_profiles
        - source_language_profiles
        - source_tags

## Plex

##### ::: buildarr_sonarr.config.import_lists.PlexWatchlistImportList
    options:
      members:
        - type
        - access_token

## Trakt

##### ::: buildarr_sonarr.config.import_lists.TraktImportList
    options:
      members:
        - access_token
        - refresh_token
        - expires
        - auth_user
        - rating
        - username
        - genres
        - years
        - limit
        - trakt_additional_parameters

### List

##### ::: buildarr_sonarr.config.import_lists.TraktListImportList
    options:
      members:
        - type
        - list_name

### Popular List

##### ::: buildarr_sonarr.config.import_lists.TraktPopularlistImportList
    options:
      members:
        - type
        - list_type

### User

##### ::: buildarr_sonarr.config.import_lists.TraktUserImportList
    options:
      members:
        - type
        - list_type
