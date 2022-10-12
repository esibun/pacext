from pacext.db import ensure_container
from pacext.fs import prepare_pacroot, unmount_pacroot
from pacext.runner import run_pacman
from pacext.squashfs import update_squashfs


def sync(container, packages):
    container_info = ensure_container(container)

    prepare_pacroot(container_info)

    pacman_args = [
        "--dbpath", container_info.path + "/pacdb",
        "--root", container_info.path + "/pacroot",
        "-S"
    ]

    for package in packages:
        pacman_args.append(package)

    run_pacman(pacman_args)

    unmount_pacroot(container_info)

    update_squashfs(container_info)
