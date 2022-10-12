import os
import shutil

from pacext.db import ensure_container
from pacext.fs import unmount_pacroot


def delete(container):
    container_info = ensure_container(container)

    unmount_pacroot(container_info)

    shutil.rmtree(container_info.path)

    os.remove("/home/deck/.config/pacext/db/squashfs/" + container + ".raw")
