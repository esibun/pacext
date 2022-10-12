import click
import os
import shutil
from types import SimpleNamespace


def ensure_container(container):
    # TODO: this should come from db, not hardcoded path
    container_info = SimpleNamespace(
        name=container,
        path="/home/deck/.config/pacext/db/storage/" + container
    )

    if not os.path.exists(container_info.path):
        click.echo("Initializing container " + container + "...")

        os.makedirs(container_info.path)

        db = container_info.path + "/pacdb"
        shutil.copytree("/var/lib/pacman", db)

        root = container_info.path + "/root"
        os.makedirs(root)

    return container_info
