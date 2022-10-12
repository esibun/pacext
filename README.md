# Pacext

Install Pacman/AUR packages on a read-only /usr or /opt using Systemd SYSEXT.

This package is being written as an alternative to OverlayFS approaches - although SYSEXT technically uses OverlayFS on the backend, it is easier to manage changes as containers, and changes can be quickly reverted by simply removing the container.

## WARNING

**This software is alpha quality.  I am not responsible for loss of data, dead drives, thermonuclear war, etc.  Use of this software is at your own risk.**

Known issues:
- File removals seem to be broken - pacman seems to do this for library updates
- Root path is hardcoded in multiple places as DB support isn't implemented yet
- Installer is not functional yet
- No AUR support yet

If you still want to use this software in its current state, checkout the software to `/home/deck/.config/pacext` and create a symlink from `/var/lib/extensions` to `/home/deck/.config/pacext/db/squashfs`.  Usage with other operating systems will require code changes for now.

## Installation

Copy the repository to a writable area on the disk and run `./install.sh`.  The installer will create the necessary symlinks and initialize the package database for you.

## Usage

Usage is similar to Pacman, but requires you to specify a SYSEXT container.  In general, it is recommended to keep only related packages in the same container so package cleanup is easier.

The package is still under development, but the following commands are supported:

### Install a package to a container
```
pacext devel -S base-devel
```

### Delete an entire container
```
pacext devel -D
```

### Cleanup container tempfiles (normally shouldn't be necessary)
*(Subject to change)*
```
pacext "" -C
```
