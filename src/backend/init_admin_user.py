#!/usr/bin/env python3
"""Initialize the default admin user in the database.

This mirrors scripts/create_admin.py but is designed to be safe
to run multiple times without resetting existing credentials.
"""

import os

from app.core.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash


def main() -> None:
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", f"{admin_username}@localhost")

    db = SessionLocal()
    try:
        admin = (
            db.query(User)
            .filter(User.username == admin_username)
            .first()
        )
        if admin:
            print(
                f"\u2713 Admin user '{admin_username}' already exists; "
                "leaving credentials unchanged"
            )
            return

        hashed_password = get_password_hash(admin_password)
        admin = User(
            username=admin_username,
            email=admin_email,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
            totp_enabled=False,
            totp_secret=None,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"\u2713 Created default admin user '{admin_username}'")
    except Exception as exc:  # pragma: no cover - init helper
        db.rollback()
        print(f"\u2717 Failed to initialize admin user: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

