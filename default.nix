# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0
{
  lib,
  buildPythonPackage,
  garminconnect,
  setuptools-scm,
  setuptools,
  stravalib,
  stravaweblib,
  thefuzz,
  pillow,
}:
buildPythonPackage rec {
  pname = "strava2garminconnect";
  version = "0.1.0";
  pyproject = true;
  src = ./.;

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    stravalib
    stravaweblib
    garminconnect
    thefuzz
    pillow
  ];

  meta = {
    changelog = "https://github.com/stv0g/strava2garminconnect/releases/tag/${version}";
    description = "Synchronize Strava activities to Garmin Connect";
    homepage = "https://github.com/stv0g/strava2garminconnect";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [
      stv0g
    ];
  };
}
