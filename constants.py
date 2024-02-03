import stat
from pathlib import Path
from typing import Any

BASE_DATA_PATH = Path("/var/lib/yukkuricraft")
REPO_ROOT_PATH = Path(__file__).parent.parent.parent  # G w o s s

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
