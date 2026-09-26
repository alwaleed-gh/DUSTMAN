from pathlib import Path


HOME_DIR = Path.home()

TARGETS = [
    HOME_DIR / "Downloads",
    HOME_DIR / ".cache",
    HOME_DIR / ".local/share/Trash",
    Path("/tmp"),
    Path("/var/tmp"),
]


DEFAULT_MAX_AGE_DAYS = 7