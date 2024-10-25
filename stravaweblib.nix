# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0
{
  lib,
  pythonOlder,
  buildPythonPackage,
  fetchFromGitHub,
  stravalib,
  beautifulsoup4,
  setuptools,
  setuptools-scm,
  ...
}:

buildPythonPackage rec {
  pname = "stravaweblib";
  version = "0.0.8";

  disabled = pythonOlder "3.4";

  src = fetchFromGitHub {
    owner = "pR0Ps";
    repo = "stravaweblib";
    rev = "refs/tags/v${version}";
    hash = "sha256-v54UeRjhoH0GN2AVFKRjqKJ6BYUXVATe2qoDk9P48oU=";
  };

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    stravalib
    beautifulsoup4
  ];

  pythonImportsCheck = [ "stravaweblib" ];

  meta = with lib; {
    description = "Python library for extending the Strava v3 API using web scraping";
    homepage = "https://github.com/pR0Ps/stravaweblib";
    license = licenses.mpl20;
    maintainers = with maintainers; [ stv0g ];
  };
}
