# Release Notes

## [v0.4.0](https://github.com/buildarr/buildarr-sonarr/releases/tag/v0.4.0) - 2023-03-27

This is the first release of the Sonarr plugin for Buildarr as an independent package.

### Added

* Implement testing of cached and fetched instance secrets ([#32](https://github.com/buildarr/buildarr/pull/32))
* Refactor the internals of Buildarr to improve maintainability ([#30](https://github.com/buildarr/buildarr/pull/30))

### Changed

* Convert `Password` and `SonarrApiKey` to subclasses of `SecretStr` ([#34](https://github.com/buildarr/buildarr/pull/34))
* Fix CLI exception class inheritance ([#35](https://github.com/buildarr/buildarr/pull/35))
* Use discriminated unions to accurately determine resource type ([#36](https://github.com/buildarr/buildarr/pull/36))
* Change log types of some TRaSH logs to `INFO` ([#37](https://github.com/buildarr/buildarr/pull/37))
* Add support for generating Docker Compose services ([buildarr/buildarr#73](https://github.com/buildarr/buildarr/pull/73))
* Fork the Sonarr plugin into a separate package ([#1](https://github.com/buildarr/buildarr-sonarr/pull/1))


## [v0.3.0](https://github.com/buildarr/buildarr/releases/tag/v0.3.0) - 2023-03-15

This is a feature and bugfix release that extends the groundwork laid in the previous version for making Buildarr more usable, and future-proof for the planned new plugins.

The major new feature this release introduces is instance linking: the ability to define relationships between two instances.

Most of the work went into the internal implementation to make it possible to use in plugins, but one use case within the Sonarr plugin itself is now supported: [Sonarr instances using another Sonarr instance](plugins/sonarr/configuration/import-lists.md#sonarr) as an import list, via the new [`instance_name`](plugins/sonarr/configuration/import-lists.md#buildarr.plugins.sonarr.config.import_lists.SonarrImportList.instance_name) attribute.

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
    * `source_quality_profile_ids` renamed to [`source_quality_profiles`](plugins/sonarr/configuration/import-lists.md#buildarr.plugins.sonarr.config.import_lists.SonarrImportList.source_quality_profiles)
    * `source_language_profile_ids` renamed to [`source_language_profiles`](plugins/sonarr/configuration/import-lists.md#buildarr.plugins.sonarr.config.import_lists.SonarrImportList.source_language_profiles)
    * `source_tag_ids` renamed to [`source_tags`](plugins/sonarr/configuration/import-lists.md#buildarr.plugins.sonarr.config.import_lists.SonarrImportList.source_tags)
* Improve Sonarr quality definition [`min` and `max`](plugins/sonarr/configuration/quality.md#buildarr.plugins.sonarr.config.quality.QualityDefinition.min) validation so that `400` is also a valid value for `max`, and enforce `min`-`max` value difference constraints
* Major internal code refactor through the introduction of [Ruff](https://beta.ruff.rs/docs) to the development pipeline, fixing a large number of minor code quality issues

### Changed

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

### Changed

* Update dependency versions ([buildarr/buildarr@3c19ede](https://github.com/buildarr/buildarr/commit/3c19ede))
* Add missing download client documentation ([buildarr/buildarr@d07936f](https://github.com/buildarr/buildarr/commit/d07936f))
* Fix incorrect config value definition in docs ([buildarr/buildarr@d1807a0](https://github.com/buildarr/buildarr/commit/d1807a0))
* Clean up and update Sonarr plugin internals ([buildarr/buildarr#14](https://github.com/buildarr/buildarr/pull/14))
* Fix updates to Sonarr quality definitions ([buildarr/buildarr#15](https://github.com/buildarr/buildarr/pull/15))
* Fix updates to Sonarr backup general settings ([buildarr/buildarr#16](https://github.com/buildarr/buildarr/pull/16))


## [v0.1.0](https://github.com/buildarr/buildarr/releases/tag/v0.1.0) - 2023-02-11

Release the initial version of Buildarr (v0.1.0).
