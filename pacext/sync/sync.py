from pacext.db import ensure_container
from pacext.fs import prepare_pacroot, unmount_pacroot
from pacext.runner import run_pacman
from pacext.squashfs import update_squashfs


def pre_oper(container):
    container_info = ensure_container(container)

    prepare_pacroot(container_info)

    return container_info

def post_oper(container_info):
    unmount_pacroot(container_info)

    update_squashfs(container_info)

def sync(container, packages):
    container_info = pre_oper(container)

    pacman_args = [
        "--dbpath", container_info.path + "/pacdb",
        "--root", container_info.path + "/pacroot",
        "-S", "--overwrite=*"
    ]

    for package in packages:
        pacman_args.append(package)

    run_pacman(pacman_args)

    post_oper(container_info)

def upgrade(container, args):
    container_info = pre_oper(container)

    pacman_args = [
        "--dbpath", container_info.path + "/pacdb",
        "--root", container_info.path + "/pacroot",
        "-U", "--overwrite=*"
    ]

    for arg in args:
        pacman_args.append(arg)

    run_pacman(pacman_args)

    post_oper(container_info)
