# strava2garminconnect: Synchronize Strava activities to Garmin Connect

strava2garminconnect is a command line application to synchronize activities from Strava to Garmin Connect.

Synchronization from Garmin Connect to Strava is long established and officially supported by Garmin.
However, this is not true for the reverse direction which would be quite useful for importing activity data from Fitness apps which have Strava, by lack Garmin Connect integration.

An example which motivated this tools are MyWhoosh.

But luckily, with some web scraping we can retrieve the original FIT, GPX or TCX files from Strava and import them to Garmin Connect as new activities.

In addition this script manually synchronizes:

- the activity name as provided in Strava
- the activity photos
- the gear used in the activity (planned)

## Authors

- Steffen Vogel <post@steffenvogel.de>

## License

strava2garminconnect is licensed under the [Apache-2.0 license](LICENSES/Apache-2.0.txt).

- SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
- SPDX-License-Identifier: Apache-2.0
