import glob
import os
import shutil

from pacext.db import ensure_container
from subprocess import run

DEVICE_BUSY = 16


def mount_readonly(container_info, name, path):
    pass  # not sure if this is possible atm


def mount_direct(container_info, name, path):
    cd = container_info.path + "/pacroot/"
    os.makedirs(cd + name)
    run(["mount", "--bind", path, cd + name])


def mount_overlay(container_info, name, lower):
    cd = container_info.path + "/pacroot/"
    pd = container_info.path + "/"

    # make pacroot dir
    os.makedirs(cd + name)

    # make upper dir
    os.makedirs(pd + "root/" + name, exist_ok=True)

    # make work dir
    os.makedirs(pd + "ofswork/work-" + name)

    args = ["mount",
            "-t",
            "overlay",
            "overlay",
            "-o",
            "lowerdir=" + lower +
            ",upperdir=" + pd + "root/" + name +
            ",workdir=" + pd + "ofswork/work-" + name,
            cd + name]
    print(" ".join(args))
    run(args)


def mount_special(container_info, name):
    cd = container_info.path + "/pacroot/"
    if name == "dev":
        os.makedirs(cd + "dev")
        run(["mount", "--rbind", "/dev", cd + "dev"])
        run(["mount", "--make-rslave", "/dev"])
    if name == "proc":
        os.makedirs(cd + "proc")
        run(["mount", "--types", "proc", "/proc", cd + "proc"])
    if name == "sys":
        os.makedirs(cd + "sys")
        run(["mount", "--rbind", "/sys", cd + "sys"])
        run(["mount", "--make-rslave", "/sys"])
    if name == "tmp":
        os.makedirs(cd + "tmp")
        run(["mount", "--rbind", "/tmp", cd + "tmp"])


def symlink_rel(container_info, name, target):
    run(["ln", "-s", target,
         container_info.path + "/pacroot" + name])


def prepare_pacroot(container_info):
    # unmount everything in case directory is dirty
    unmount_pacroot(container_info)

    # make pacman root dir
    os.makedirs(container_info.path + "/pacroot")

    # make OverlayFS working root
    os.makedirs(container_info.path + "/ofswork")

    # mount filesystem dirs as appropriate

    symlink_rel(container_info, "/bin", "usr/bin")
    mount_direct(container_info, "boot", "/boot")
    mount_special(container_info, "dev")
    mount_direct(container_info, "efi", "/efi")
    mount_direct(container_info, "esp", "/esp")
    mount_direct(container_info, "etc", "/etc")
    mount_direct(container_info, "home", "/home")
    symlink_rel(container_info, "/lib", "usr/lib")
    symlink_rel(container_info, "/lib64", "usr/lib")
    symlink_rel(container_info, "/mnt", "var/mnt")
    mount_overlay(container_info, "opt", "/opt")
    mount_special(container_info, "proc")
    mount_direct(container_info, "root", "/root")
    mount_direct(container_info, "run", "/run")
    symlink_rel(container_info, "/sbin", "usr/bin")
    mount_direct(container_info, "srv", "/srv")
    mount_special(container_info, "sys")
    mount_special(container_info, "tmp")
    mount_overlay(container_info, "usr", "/usr")
    mount_direct(container_info, "var", "/var")


def unmount_pacroot(container_info):
    for g in glob.glob(container_info.path + "/pacroot/*"):
        proc = run(["umount", g], capture_output=True)
        if b"target is busy" in proc.stderr:
            print("force unmounting")
            run(["umount", "-l", g])
    for d in ["boot", "dev", "efi", "esp", "etc", "home", "opt", "proc",
              "root", "run", "srv", "sys", "tmp", "usr", "var"]:
        try:
            os.rmdir(container_info.path + "/pacroot/" + d)
        except FileNotFoundError:
            pass
    for s in ["bin", "lib", "lib64", "mnt", "sbin"]:
        try:
            os.remove(container_info.path + "/pacroot/" + s)
        except FileNotFoundError:
            pass
    try:
        os.rmdir(container_info.path + "/pacroot")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(container_info.path + "/ofswork")
    except FileNotFoundError:
        pass


def unmount_all():
    for c in glob.glob("/home/deck/.config/pacext/db/storage/*"):
        name = os.path.basename(c)

        container_info = ensure_container(name)

        unmount_pacroot(container_info)
