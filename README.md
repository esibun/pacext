# Pacext

Install Pacman/AUR packages on a read-only /usr or /opt using Systemd SYSEXT.

This package is being written as an alternative to OverlayFS approaches

## Installation

Copy the repository to a writable area on the disk and run `./install.sh`.  The installer will create the necessary symlinks and initialize the package database for you.

## Usage

Usage is similar to Pacman, but requires you to specify a SYSEXT container.  In general, it is recommended to keep only related packages in the same container so package cleanup is easier.

The package is still under development, but the following commands are supported:

### Install a package to a container
```
pacext devel -S base-devel
```
