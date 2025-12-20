import json
from pathlib import Path
from typing import Any

from app.config import settings


LOG_DIR = Path(settings.log_dir)
LOG_DIR.mkdir(exist_ok=True)


def audit_log(**record: Any) -> None:
    record["schema_version"] = "v1"
    log_file = LOG_DIR / "audit.log"

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
