#!/usr/bin/env python3
"""Initialize core system settings in the database.

This mirrors the behaviour of the installer, making sure that
app_name and app_version keys exist in the system_settings table.

The script is safe to run multiple times (idempotent).
"""

import os
from typing import Optional

from app.core.database import SessionLocal
from app.models.database import SystemSettings


def upsert_setting(db, key: str, value: str, description: Optional[str] = None) -> None:
    """Insert or update a single setting row by key."""
    setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    if setting:
        setting.value = value
        if description is not None:
            setting.description = description
    else:
        setting = SystemSettings(key=key, value=value, description=description)
        db.add(setting)


def main() -> None:
    app_version = os.getenv("APP_VERSION", "1.1.9")

    db = SessionLocal()
    try:
        upsert_setting(
            db,
            "app_version",
            app_version,
            "Current application version",
        )
        upsert_setting(
            db,
            "app_name",
            "Depl0y",
            "Application name",
        )
        db.commit()
        print("\u2713 System settings initialized/updated")
    except Exception as exc:  # pragma: no cover - init helper
        db.rollback()
        print(f"\u2717 Failed to initialize system settings: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

