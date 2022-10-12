import os
import subprocess
from dotenv import dotenv_values


def update_squashfs(container_info):
    name = container_info.name
    root = container_info.path + "/root"

    try:
        os.remove("/home/deck/.config/pacext/db/squashfs/" + name + ".raw")
    except FileNotFoundError:
        pass

    # Create required SYSEXT metadata
    osinfo = dotenv_values("/etc/os-release")
    os.makedirs(root + "/usr/lib/extension-release.d", exist_ok=True)
    with open(root + "/usr/lib/extension-release.d/extension-release." + name, "w") as f:
        f.write("ID=" + osinfo["ID"] + "\n")
        f.write("VERSION_ID=" + osinfo["VERSION_ID"])

    # TODO: don't hardcode the squashfs path
    subprocess.run(
        ["mksquashfs", root, "/home/deck/.config/pacext/db/squashfs/" + name + ".raw"])
    subprocess.run(["systemd-sysext", "refresh"])
