# Release Notes (Buildarr Sonarr Plugin)

## [v0.6.4](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.6.4) - 2024-03-02

This release addresses an issue where Buildarr would try to always try to create new remote path mappings on a Sonarr instance in certain cases, even if they already existed, resulting in an API error.
Path handling for remote path mappings within Buildarr has also been improved, making sure that Buildarr will handle them correctly for both POSIX paths and Windows paths (for Sonarr instances running on Windows).

It also improves error handling for Sonarr API responses, making error messages output from the API easier to understand when output by Buildarr.

### Changed

* Functionise host URL generation in secrets ([#47](https://github.com/buildarr/buildarr-sonarr/pull/47))
* Improve JSON API response error handling ([#48](https://github.com/buildarr/buildarr-sonarr/pull/48))
* Update Poetry and lock file ([#54](https://github.com/buildarr/buildarr-sonarr/pull/54))
* Fix remote path mapping checking edge cases ([#56](https://github.com/buildarr/buildarr-sonarr/pull/56))


## [v0.6.3](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.6.3) - 2023-12-02

This release adds support for defining a URL base for the Sonarr instance in the Buildarr configuration, using the `url_base` host configuration attribute.

This allows Sonarr instances with APIs available under a custom path (e.g. `http://localhost:8989/sonarr`) to be managed by Buildarr.

### Changed

* Add Sonarr instance URL base support ([#44](https://github.com/buildarr/buildarr-sonarr/pull/44))


## [v0.6.2](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.6.2) - 2023-12-01

This release fixes the following issues:

* Fix an issue where default values for attributes in qBittorrent download clients were not used when the value is not provided by Sonarr API, resulting in qBittorrent download clients being unable to be managed.

### Changed

* Fix reading remote attributes for qBittorrent download clients ([#40](https://github.com/buildarr/buildarr-sonarr/pull/40))


## [v0.6.1](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.6.1) - 2023-11-13

This release fixes the following issues:

* Permanently fix Torznab/Newznab indexer category parsing by making it not error when an unknown category ID is found on the remote instance.
* Allow the Sonarr-native category name (e.g. `TV/WEB-DL`) to be defined directly in Buildarr, instead of the Buildarr-native names (e.g. `TV-WEBDL`). The old names are still supported.
* Fix dumping Sonarr instance configurations using the CLI, which was failing due to a validation regression introduced in the previous release.

The CLI command for dumping Sonarr instance configurations has also been improved, and can now auto-fetch Sonarr instance API keys by simply leaving the API key blank, and pressing Enter when prompted. Note that this will only work on Sonarr instances that have authentication disabled.

As this release of the Sonarr plugin uses the latest plugin API features, Buildarr v0.7.1 or later is required for this release.

### Changed

* Auto-fetch API key when dumping configuration if not specified ([#35](https://github.com/buildarr/buildarr-sonarr/pull/35))
* Fix Newznab/Torznab indexer bugs ([#36](https://github.com/buildarr/buildarr-sonarr/pull/36))


## [v0.6.0](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.6.0) - 2023-11-12

This updates the Sonarr plugin so that it is compatible with [Buildarr v0.7.0](https://buildarr.github.io/release-notes/#v070-2023-11-12).

### Changed

* Add Buildarr v0.7.0 support ([#31](https://github.com/buildarr/buildarr-sonarr/pull/31))


## [v0.5.4](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.5.4) - 2023-11-05

This is a minor release that fixes the following issues:

* Fix managing Newznab/Torznab indexers that have the `TV` global category enabled (including Prowlarr-managed indexers).

### Changed

* Add the `TV` group as a selectable Newznab/Torznab category ([#27](https://github.com/buildarr/buildarr-sonarr/pull/27))


## [v0.5.3](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.5.3) - 2023-09-11

This is a minor release that fixes the following issues:

* Fix managing e-mail, Mailgun and SendGrid notification connections by enforcing that email address attributes consist only of an email address, and do not contain a name (e.g. `Sonarr Notifications <sonarr@example.com>`). Sonarr V3 does not support this style of email address definition.

### Changed

* Fix parsing email addresses for notification connections ([#23](https://github.com/buildarr/buildarr-sonarr/pull/23))


## [v0.5.2](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.5.2) - 2023-09-09

This is a minor release that fixes the following issues:

* Fix Sonarr instance configuration dumping via the CLI for some instances, by changing URL parsing for the Sonarr instance URL to accept any valid URL (not just instances with actual FQDNs).

### Changed

* Fix URL parsing for configuration dumping ([#19](https://github.com/buildarr/buildarr-sonarr/pull/19))


## [v0.5.1](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.5.1) - 2023-09-09

This is a minor release that enables support for Buildarr v0.6.0.

Buildarr v0.5.0 is still supported in this release.

### Changed

* Update package metadata and dependencies ([#15](https://github.com/buildarr/buildarr-sonarr/pull/15))


## [v0.5.0](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.5.0) - 2023-04-16

This updates the Sonarr plugin so that it is compatible with [Buildarr v0.5.0](https://buildarr.github.io/release-notes/#v050-2023-04-16).

Other changes to the Sonarr plugin for this release include:

* Fix a bug where Sonarr instance configuration dumping was broken due to trying to use a Buildarr configuration value that was not loaded
* Improve support for deleting resources with `delete_unmanaged`, by using the new `delete_remote` API function
* Remove the `sonarr.tags.delete_unused` attribute (for deleting Sonarr tags not used in Buildarr), as it was unimplemented and Sonarr automatically cleans up unused tags anyway

### Changed

* Update plugin to newer Buildarr API standards ([#11](https://github.com/buildarr/buildarr-sonarr/pull/11))


## [v0.4.1](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.4.1) - 2023-04-08

This is a bugfix release that addresses a number of issues that one might encounter when deploying a Sonarr instance
for the first time, or linking a Sonarr instance with a Prowlarr instance using the new [Prowlarr plugin for Buildarr](https://buildarr.github.io/plugins/prowlarr).

* Add mutual exclusion handling for the `category` and `directory` attributes for Transmission download clients
* Rename the `indexer_priority` attribute on indexers to `priority` (with an alias available for backwards compatibility)
* Remove the `anime_standard_format_search` attribute from the common indexer interface, and add it to the specific indexer types that implement it
* Fix a large number of indexer parsing bugs
    * Torznab indexers are now confirmed to load correctly from remote Sonarr instances (by testing the Torznab indexer Prowlarr creates)
* Fix updating delay profiles on brand new Sonarr installations
* Fix updating Media Management naming configuration
* Fix an issue where UI settings updating was not idempotent

### Changed

* Fix bugs from integration tests ([#4](https://github.com/buildarr/buildarr-sonarr/pull/4))


## [v0.4.0](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.4.0) - 2023-03-31

This is the first release of the Buildarr Sonarr plugin as an independent package.

As major strides have been taken to stabilise the plugin API, the Sonarr plugin for Buildarr has been forked into a separate package, `buildarr-sonarr`. From Buildarr version 0.4.0 onwards, application plugins are no longer bundled.

The [Docker container](https://buildarr.github.io/plugins/#installing-plugins-into-the-docker-container) still bundles the Sonarr plugin for ease of use, but when upgrading an existing [standalone installation](https://buildarr.github.io/plugins/#installing-plugins-for-a-standalone-application) of Buildarr, the Sonarr plugin package will need to be installed using `pip`.

```bash
$ pip install buildarr-sonarr
```

This will allow the Sonarr plugin to deliver releases independently of the base Buildarr package, allowing for more rapid releases of both packages, while ensuring compability between Buildarr and its plugins through plugin version pinning of the Buildarr base package.

A number of other features and bugfixes have been added in this release of the Sonarr plugin:

* Add support for [dry runs](https://buildarr.github.io/usage/#dry-runs) in Buildarr ad-hoc runs, for testing configuration changes against live instances *without* modifying them
* Add support for [automatic generation of Docker Compose files](https://buildarr.github.io/usage/#generating-a-docker-compose-file) from Buildarr configuration files using the `buildarr compose` command
* Improve validation to output easier-to-read error messages in some cases
* Refactor logging to use the new logging API for Buildarr v0.4.0 onwards

### Added

* Add the `--dry-run` option to `buildarr run` ([buildarr/buildarr#56](https://github.com/buildarr/buildarr/pull/56))
* Add instance-specific configs to global state and fix Sonarr dry-run bug ([buildarr/buildarr#59](https://github.com/buildarr/buildarr/pull/59))
* Add the `buildarr test-config` command ([buildarr/buildarr#60](https://github.com/buildarr/buildarr/pull/60))
* Add `--secrets-file` option to daemon and run modes ([buildarr/buildarr#67](https://github.com/buildarr/buildarr/pull/67))
* Add the `buildarr compose` command ([buildarr/buildarr#73](https://github.com/buildarr/buildarr/pull/73))
* Reintroduce `buildarr.__version__` and use it internally ([buildarr/buildarr#75](https://github.com/buildarr/buildarr/pull/75))
* Add `version` attribute to plugin metadata object ([buildarr/buildarr#78](https://github.com/buildarr/buildarr/pull/78))

### Changed

* Convert most root validators to attribute-specific validators ([buildarr/buildarr#54](https://github.com/buildarr/buildarr/pull/54))
* Remove unused code and fix pre-commit job ([buildarr/buildarr#58](https://github.com/buildarr/buildarr/pull/58))
* Enable validating default config/secrets attribute values ([buildarr/buildarr#63](https://github.com/buildarr/buildarr/pull/63))
* Reduce usage of `initialize.js` endpoints ([buildarr/buildarr#66](https://github.com/buildarr/buildarr/pull/66))
* Refactor logging infrastructure ([buildarr/buildarr#68](https://github.com/buildarr/buildarr/pull/68))
* Relax dependency version requirements ([buildarr/buildarr#69](https://github.com/buildarr/buildarr/pull/69))
* Improve and add missing docs for new features ([buildarr/buildarr#70](https://github.com/buildarr/buildarr/pull/70))
* Evaluate local paths relative to the config file ([buildarr/buildarr#71](https://github.com/buildarr/buildarr/pull/71))
* Add temporary ignore for `watchdog.Observer` type hint ([buildarr/buildarr#72](https://github.com/buildarr/buildarr/pull/72))
* Fork the Sonarr plugin into its own package ([#1](https://github.com/buildarr/buildarr-sonarr/pull/1))


## [v0.3.0](https://github.com/buildarr/buildarr/releases/tag/v0.3.0) - 2023-03-15

This is a feature and bugfix release that extends the groundwork laid in the previous version for making Buildarr more usable, and future-proof for the planned new plugins.

A major bug where running Buildarr when `secrets.json` does not exist would result in an error, even if valid instance credentials were found, has been fixed. This would have prevented many people from trying out Buildarr, and for this I would like to apologise.

In the future automated unit tests are planned, and major refactors of the Buildarr codebase are now less likely to happen as a result of development, so bugs like this should not happen as often in the future.

The major new feature this release introduces is instance linking: the ability to define relationships between two instances.

Most of the work went into the internal implementation to make it possible to use in plugins, but one use case within the Sonarr plugin itself is now supported: [Sonarr instances using another Sonarr instance](configuration/import-lists.md#sonarr) as an import list, via the new [`instance_name`](configuration/import-lists.md#buildarr_sonarr.config.import_lists.SonarrImportList.instance_name) attribute.

When using this attribute, Buildarr will automatically fill in the API key attribute so you don't have to, and instead of using IDs to reference quality profiles/language profiles/tags in the source instance, names can now be used:

```yaml
sonarr:
  instances:
    sonarr-hd:
      hostname: "localhost"
      port: 8989
    sonarr-4k:
      hostname: "localhost"
      port: 8990
      settings:
        import_lists:
          definitions:
            Sonarr (HD):
              type: "sonarr"
              # Global import list options.
              root_folder: "/path/to/videos"
              quality_profile: "4K"
              language_profile: "English"
              # Sonarr import list-specific options.
              full_url: "http://sonarr:8989"
              instance_name: "sonarr-hd"
              source_quality_profiles:
                - "HD/SD"
              source_language_profiles:
                - "English"
              source_tags:
                - "shows"
```

When instance links are made, Buildarr automatically adjusts the order of execution such that the target instance is always processed before the instance linking to the target. This ensures the state of the target instance is consistent when they are both updated to establish the link.

A number of other improvements and bugfixes were made, such as:

* Fix configuration validation to allow local and non-qualified domains on all URL-type attributes (fixes `localhost` API URL references)
* Rename the following Sonarr import list attributes (and retain the old names as aliases to ensure backwards compatibility):
    * `source_quality_profile_ids` renamed to [`source_quality_profiles`](configuration/import-lists.md#buildarr_sonarr.config.import_lists.SonarrImportList.source_quality_profiles)
    * `source_language_profile_ids` renamed to [`source_language_profiles`](configuration/import-lists.md#buildarr_sonarr.config.import_lists.SonarrImportList.source_language_profiles)
    * `source_tag_ids` renamed to [`source_tags`](configuration/import-lists.md#buildarr_sonarr.config.import_lists.SonarrImportList.source_tags)
* Fix reading the `$BUILDARR_LOG_LEVEL` environment variable to be case-insensitive
* Clean up runtime state after individual update runs in daemon mode, to ensure no state leakage into subsequent runs
* Add a new [`buildarr.request_timeout`](https://buildarr.github.io/configuration/#buildarr.config.buildarr.BuildarrConfig.request_timeout) configuration attribute for adjusting API request timeouts (the default is 30 seconds)
* Improve Sonarr quality definition [`min` and `max`](configuration/quality.md#buildarr_sonarr.config.quality.QualityDefinition.min) validation so that `400` is also a valid value for `max`, and enforce `min`-`max` value difference constraints
* Major internal code refactor through the introduction of [Ruff](https://beta.ruff.rs/docs) to the development pipeline, fixing a large number of minor code quality issues

### Changed

* Fix fetching new instance secrets ([buildarr/buildarr#44](https://github.com/buildarr/buildarr/pull/44))
* Accept local and non-qualified domain names in URLs ([buildarr/buildarr#46](https://github.com/buildarr/buildarr/pull/46))
* Add instance referencing and dependency resolution ([buildarr/buildarr#47](https://github.com/buildarr/buildarr/pull/47))
* Replace isort and Flake8 with Ruff and reformat source files ([buildarr/buildarr#49](https://github.com/buildarr/buildarr/pull/49))


## [v0.2.0](https://github.com/buildarr/buildarr/releases/tag/v0.2.0) - 2023-02-23

This is a feature release that comprehensively refactors the internal structure of Buildarr and the plugin API, and introduces a new, formally defined global state architecture that Buildarr and plugins can utilise.

These changes improve maintainability of the codebase, allow for more accurate type validation of global state objects, make the plugin API easier to understand for developers, and pave the way for planned new features such as configuring instance-to-instance links within Buildarr.

This release also introduces connection testing of cached and auto-retrieved instance secrets, to ensure Buildarr can communicate and authenticate with instances before it tries to update them.

A handful of bugs were fixed, including but not limited to:

* Work around a parsing bug in Pydantic that causes Buildarr to error out when specifying Sonarr instance API keys in the Buildarr configuration
* More accurate resource type detection eliminating the chance of parsing errors for Sonarr import list, indexer, download client and connection definitions
* Set better constraints on some Sonarr configuration attributes:
    * To handle suboptimal configuration (e.g. ignore duplicate elements)
    * To reject invalid configuration (e.g. require at least one recipient e-mail address on Mailgun and Sendgrid connection types)

### Added

* Implement testing of cached and fetched instance secrets ([buildarr/buildarr#32](https://github.com/buildarr/buildarr/pull/32))
* Refactor the internals of Buildarr to improve maintainability ([buildarr/buildarr#30](https://github.com/buildarr/buildarr/pull/30))

### Changed

* Convert `Password` and `SonarrApiKey` to subclasses of `SecretStr` ([buildarr/buildarr#34](https://github.com/buildarr/buildarr/pull/34))
* Fix CLI exception class inheritance ([buildarr/buildarr#35](https://github.com/buildarr/buildarr/pull/35))
* Use discriminated unions to accurately determine resource type ([buildarr/buildarr#36](https://github.com/buildarr/buildarr/pull/36))
* Change log types of some TRaSH logs to `INFO` ([buildarr/buildarr#37](https://github.com/buildarr/buildarr/pull/37))
* Set better constraints on Sonarr configuration attributes ([buildarr/buildarr#38](https://github.com/buildarr/buildarr/pull/38))


## [v0.1.2](https://github.com/buildarr/buildarr/releases/tag/v0.1.2) - 2023-02-20

This is a bugfix release that fixes updates of certain types of Sonarr instance configuration, improving usability of the Sonarr plugin.

The following types of Sonarr instance configuration have had bugfixes and improvements made, and are confirmed to work without errors:

* Media Management
    * Ensure that `minimum_free_space` is set to a minimum of 100 MB
    * Fix `unmonitor_deleted_episodes` so that it is now checked and updated by Buildarr
    * Add a `delete_unmanaged_root_folders` option to allow Buildarr to delete undefined root folders (disabled by default)
    * Improve other configuration constraints so that it more closely matches Sonarr
    * Fix a minor logging bug in root folder updates
* Profiles
    * Quality Profiles / Language Profiles
        * Improve attribute constraints e.g. ensure duplicate quality values cannot be defined, enforce `upgrade_until` being required when `allow_upgrades` is `True`
        * Fix conversion between Buildarr and Sonarr configuration state so that no errors occur when upgrades are disabled
        * Internal refactor to make the code easier to understand
    * Delay Profiles - Confirmed to work properly as of `v0.1.1` (and likely `v0.1.0`)
    * Release Profiles
        * Fix bug introduced in `v0.1.1` where internal validation is not done on release profiles downloaded from TRaSH-Guides, resulting in preferred word lists being updated on each run, and potential errors not being caught if there are invalid values in the profile
        * Internal refactor to simplify implementation
* Quality
    * Fix bug introduced in `v0.1.1` where internal validation is not done on quality profiles downloaded from TRaSH-Guides, resulting in potential errors not being caught if there are invalid values in the profile
* Metadata - Confirmed to work properly as of `v0.1.1` (and likely `v0.1.0`)
    * Small logging bug fixed where it was ambiguous which metadata type was being modified on update
* Tags - Confirmed to work properly as of `v0.1.1` (and likely `v0.1.0`)
* General
    * Improve behaviour when setting an authentication username and password so that configuration updates are idempotent when authentication is disabled
    * Fix setting a proxy password
    * Fix setting backup intervals and retentions so that it is no longer possible to set a value not supported by Sonarr

Incorrect syntax in some examples in the documentation were also found and fixed.

### Added

* Added the `sonarr.settings.media_management.delete_unmanaged_root_folders` configuration attribute ([buildarr/buildarr#24](https://github.com/buildarr/buildarr/pull/24))

### Changed

* Improve and fix Sonarr general settings configuration updates ([buildarr/buildarr#19](https://github.com/buildarr/buildarr/pull/19))
* Fix Sonarr UI settings updates ([buildarr/buildarr#20](https://github.com/buildarr/buildarr/pull/20))
* Fix small bug Sonarr metadata definition update logging ([buildarr/buildarr#21](https://github.com/buildarr/buildarr/pull/21))
* Improve Sonarr quality profile definition parsing ([buildarr/buildarr#22](https://github.com/buildarr/buildarr/pull/22))
* Make improvements and bug fixes to quality/language/release profile and quality definition parsing ([buildarr/buildarr#23](https://github.com/buildarr/buildarr/pull/23))
* Fix Sonarr media management settings and improve root folder handling ([buildarr/buildarr#24](https://github.com/buildarr/buildarr/pull/24))


## [v0.1.1](https://github.com/buildarr/buildarr/releases/tag/v0.1.1) - 2023-02-19

This is a support release that fixes quality definition and backup configuration updates
on remote Sonarr instances.

A new Dummy plugin is now included with Buildarr, used for testing Buildarr and its
plugin API, and also serves as a reference implementation for plugin developers.

Other behind-the-scenes improvements include a refactor of the plugin API to allow
for accurate type hints for configuration objects in secrets metadata classes
(and vice versa), and numerous updates to the documentation to correct errors
and add more detail.

### Added

* Add a GitHub Action to push releases to PyPI ([buildarr/buildarr#11](https://github.com/buildarr/buildarr/pull/11))
* Create a `buildarr-dummy` plugin for testing the Buildarr plugin API ([buildarr/buildarr#12](https://github.com/buildarr/buildarr/pull/12))

### Changed

* Fix $PUID and $GUID declarations ([b5110f3](https://github.com/buildarr/buildarr/commit/b5110f3))
* Fix Docker Hub link ([be0ba12](https://github.com/buildarr/buildarr/commit/be0ba12))
* Fix Docker volume mount docs ([fe328aa](https://github.com/buildarr/buildarr/commit/fe328aa))
* Fix troubleshooting Buildarr run docs ([e3b8833](https://github.com/buildarr/buildarr/commit/e3b8833))
* Update dependency versions ([3c19ede](https://github.com/buildarr/buildarr/commit/3c19ede))
* Fix debug Docker command in the GitHub Pages site ([1e17741](https://github.com/buildarr/buildarr/commit/1e17741))
* Disable automatic dependency version updates ([c5c61cd](https://github.com/buildarr/buildarr/commit/c5c61cd))
* Add missing download client documentation ([d07936f](https://github.com/buildarr/buildarr/commit/d07936f))
* Fix incorrect config value definition in docs ([d1807a0](https://github.com/buildarr/buildarr/commit/d1807a0))
* Fix to-do list indenting ([bca56e5](https://github.com/buildarr/buildarr/commit/bca56e5))
* Add a link to the configuration documentation in README.md ([a5c0e6d](https://github.com/buildarr/buildarr/commit/a5c0e6d))
* Clean up and update Sonarr plugin internals ([buildarr/buildarr#14](https://github.com/buildarr/buildarr/pull/14))
* Fix updates to Sonarr quality definitions ([buildarr/buildarr#15](https://github.com/buildarr/buildarr/pull/15))
* Fix updates to Sonarr backup general settings ([buildarr/buildarr#16](https://github.com/buildarr/buildarr/pull/16))

### Removed

* Removed `buildarr.__version__` (please use [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html#distribution-versions) instead)


## [v0.1.0](https://github.com/buildarr/buildarr/releases/tag/v0.1.0) - 2023-02-11

Release the initial version of Buildarr (v0.1.0).
