# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0
{
  description = "Nix flake for strava2garminconnect";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    let
      overlay =
        final: prev:
        let
          pythonOverlay = python-final: python-prev: {
            stravaweblib = python-final.callPackage ./stravaweblib.nix { };
            strava2garminconnect = python-final.callPackage ./default.nix { };
          };
        in
        {
          pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [ pythonOverlay ];

          strava2garminconnect = final.python3.pkgs.strava2garminconnect;
        };
    in
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ overlay ];
        };
      in
      {
        packages = rec {
          default = strava2garminconnect;
          inherit (pkgs) strava2garminconnect;
        };
        devShells.default = pkgs.callPackage ./shell.nix { };
      }
    )
    // {
      overlays.default = overlay;
    };
}
