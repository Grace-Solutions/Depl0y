#!/usr/bin/env sh
set -e

APP_PORT="${APPLICATION_PORT_INTERNAL:-8080}"

# Ensure core data directories exist (may be bind-mounted)
mkdir -p /var/lib/depl0y/db \
         /var/lib/depl0y/cloud-images \
         /var/lib/depl0y/isos \
         /var/lib/depl0y/ssh_keys \
         /var/lib/depl0y/cloud-init \
         /var/log/depl0y

echo "Initializing database schema..."
python - <<'PY'
from app.core.database import init_db

init_db()
PY
echo "Database schema initialized."

echo "Initializing system settings..."
python /opt/depl0y/backend/init_system_settings.py || echo "Warning: system settings initialization failed"
echo "System settings initialization step completed."

echo "Ensuring default admin user exists..."
python /opt/depl0y/backend/init_admin_user.py || echo "Warning: admin user initialization failed"
echo "Admin user initialization step completed."

echo "Starting Depl0y backend with uvicorn on port ${APP_PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${APP_PORT}"

