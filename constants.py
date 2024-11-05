import os
import stat
from pathlib import Path


BASE_DATA_PATH = Path(
    os.getenv("MC_FS_ROOT", "/couldnotfindvalidminecraftfilesystemroot")
)
"""The base path all YC data on the host filesystem will be stored.
Usually /var/lib/yukkuricraft
"""

REPO_ROOT_PATH = Path(__file__).parent.parent.parent  # G w o s s
"""The root path of the repo WITHIN the container

Usually /app/
"""

HOST_REPO_ROOT_PATH = Path(
    os.getenv("HOST_YC_REPO_ROOT", "/couldnotfindavalidhostrepopath/")
)
"""The root path of the repo OUTSIDE the container, ie host filesystem

Eg, /home/minecraft/Yukkuricraft/Yukkuricraft
"""

RESTIC_REPO_PATH = Path("/media/backups-primary/restic")
"""Path to the Restic repo
"""

VELOCITY_FORWARDING_SECRET_PATH: Path = (
    REPO_ROOT_PATH / "secrets" / "velocity" / "forwarding.secret"
)
"""Path to the Velocity forwarding secret file used to configure velocity.
"""

DEFAULT_CHMOD_MODE = (
    stat.S_IRUSR
    | stat.S_IWUSR
    | stat.S_IXUSR
    | stat.S_IRGRP
    | stat.S_IWGRP
    | stat.S_IXGRP
    | stat.S_IROTH
    | stat.S_IXOTH
)
"""The default chmod mode we apply to new files we create

Represents mode 775
"""

YC_CONTAINER_TYPE_LABEL = "net.yukkuricraft.container_type"
"""The docker label identifier representing the container type 
"""

YC_CONTAINER_NAME_LABEL = "net.yukkuricraft.container_name"
"""The docker label identifier representing the container name
"""

YC_ENV_LABEL = "net.yukkuricraft.env"
"""The docker label identifier representing the env name
"""

MC_DOCKER_CONTAINER_NAME_FMT = "YC-{env}-{name}"
"""Format string for docker container names
"""
