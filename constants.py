import os
import stat
from pathlib import Path
from typing import Any

BASE_DATA_PATH = Path(
    os.getenv("MC_FS_ROOT", "/couldnotfindvalidminecraftfilesystemroot")
)
REPO_ROOT_PATH = Path(__file__).parent.parent.parent  # G w o s s
HOST_REPO_ROOT_PATH = Path(
    os.getenv("HOST_YC_REPO_ROOT", "/couldnotfindavalidhostrepopath/")
)
RESTIC_REPO_PATH = Path("/media/backups-primary/restic")

VELOCITY_FORWARDING_SECRET_PATH: Path = (
    REPO_ROOT_PATH / "secrets" / "velocity" / "forwarding.secret"
)

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

YC_CONTAINER_TYPE_LABEL = "net.yukkuricraft.container_type"
YC_CONTAINER_NAME_LABEL = "net.yukkuricraft.container_name"
YC_ENV_LABEL = "net.yukkuricraft.env"

MC_DOCKER_CONTAINER_NAME_FMT = "YC-{env}-{name}"
