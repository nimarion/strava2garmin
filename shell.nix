# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0
{
  mkShellNoCC,
  strava2garminconnect,
  reuse,
}:
mkShellNoCC {
  inputsFrom = [
    strava2garminconnect
  ];

  packages = [
    reuse
  ];
}
