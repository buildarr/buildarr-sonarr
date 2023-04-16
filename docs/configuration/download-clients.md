# Download Clients

##### ::: buildarr_sonarr.config.download_clients.SonarrDownloadClientsSettingsConfig
    options:
      members:
        - enable_completed_download_handling
        - redownload_failed
        - delete_unmanaged
        - definitions
        - remote_path_mappings

!!! note

    Before Sonarr can send requests to download clients, at least one Usenet or
    torrent [indexer](indexers.md) will need to be configured.
    Sonarr will then send download requests to a compatible client,
    or the download client the indexer has been assigned to.

## Configuring download clients

##### ::: buildarr_sonarr.config.download_clients.download_clients.DownloadClient
    options:
      members:
        - enable
        - priority
        - remove_completed_downloads
        - remove_failed_downloads
        - tags

## Usenet download clients

These download clients retrieve media using the popular [Usenet](https://en.wikipedia.org/wiki/Usenet) discussion and content delivery system.

## Download Station

##### ::: buildarr_sonarr.config.download_clients.download_clients.DownloadstationUsenetDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

## NZBGet

##### ::: buildarr_sonarr.config.download_clients.download_clients.NzbgetDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - recent_priority
        - older_priority
        - add_paused

## NZBVortex

##### ::: buildarr_sonarr.config.download_clients.download_clients.NzbvortexDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - recent_priority
        - older_priority

## Pneumatic

##### ::: buildarr_sonarr.config.download_clients.download_clients.PneumaticDownloadClient
    options:
      members:
        - type
        - nzb_folder
        - strm_folder

## SABnzbd

##### ::: buildarr_sonarr.config.download_clients.download_clients.SabnzbdDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - recent_priority
        - older_priority

## Usenet Blackhole

##### ::: buildarr_sonarr.config.download_clients.download_clients.UsenetBlackholeDownloadClient
    options:
      members:
        - type
        - nzb_folder
        - watch_folder

## Torrent download clients

These download clients use the [BitTorrent](https://en.wikipedia.org/wiki/BitTorrent)
peer-to-peer file sharing protocol to retrieve media files.

## Aria2

##### ::: buildarr_sonarr.config.download_clients.download_clients.Aria2DownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - rpc_path
        - secret_token

## Deluge

##### ::: buildarr_sonarr.config.download_clients.download_clients.DelugeDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority

## Download Station

##### ::: buildarr_sonarr.config.download_clients.download_clients.DownloadstationTorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

## Flood

##### ::: buildarr_sonarr.config.download_clients.download_clients.FloodDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - destination
        - flood_tags
        - postimport_tags
        - additional_tags
        - start_on_add

## Hadouken

##### ::: buildarr_sonarr.config.download_clients.download_clients.HadoukenDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category

## qBittorrent

##### ::: buildarr_sonarr.config.download_clients.download_clients.QbittorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority
        - initial_state
        - sequential_order
        - first_and_last_first

## RTorrent (ruTorrent)

##### ::: buildarr_sonarr.config.download_clients.download_clients.RtorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority
        - add_stopped

## Torrent Blackhole

##### ::: buildarr_sonarr.config.download_clients.download_clients.TorrentBlackholeDownloadClient
    options:
      members:
        - type
        - torrent_folder
        - watch_folder
        - save_magnet_files
        - magnet_file_extension
        - read_only

## Transmission/Vuze

Transmission and Vuze use the same configuration parameters.

To use Transmission, set the `type` attribute in the download client to `transmission`.

To use Vuze, set the `type` attribute in the download client to `vuze`.

##### ::: buildarr_sonarr.config.download_clients.download_clients.TransmissionDownloadClientBase
    options:
      members:
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - directory
        - recent_priority
        - older_priority
        - add_paused

## uTorrent

##### ::: buildarr_sonarr.config.download_clients.download_clients.UtorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority
        - initial_state

## Configuring remote path mappings

##### ::: buildarr_sonarr.config.download_clients.remote_path_mappings.SonarrRemotePathMappingsSettingsConfig
    options:
      members:
        - delete_unmanaged
        - definitions

### Remote path mapping parameters

##### ::: buildarr_sonarr.config.download_clients.remote_path_mappings.RemotePathMapping
    options:
      members:
        - host
        - remote_path
        - local_path
        - ensure
