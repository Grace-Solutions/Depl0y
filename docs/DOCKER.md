# Docker Deployment Modes for Depl0y

This document describes the supported Docker deployment modes and how they map to the original `install.sh` behavior.

## 1. Combined stack (recommended simple deployment)

**Path:** `deployment/docker/combined`

- Image: `Agit8or/Depl0y`
- Single container running **uvicorn (backend)** and **nginx (frontend + /api proxy)**.
- Mirrors the original installer:
  - Backend (FastAPI/uvicorn) listens on `127.0.0.1:8000` **inside** the container.
  - nginx listens on `8080` in the container, serves the SPA, and proxies `/api` to `127.0.0.1:8000`.

**Start:**

```bash
cd deployment/docker/combined
docker compose up -d
```

**Access:** `http://<host>:8080`

### Data & paths

The container uses the same logical paths as the installer:

- Backend code: `/opt/depl0y/backend`
- Frontend dist: `/opt/depl0y/frontend/dist`
- DB and data: `/var/lib/depl0y/...`
- Logs: `/var/log/depl0y/...`

The compose file bind-mounts these under:

- Root: `/custom/docker/stacks` (or `${STACK_BINDMOUNTROOT}`)
- Stack-specific subfolder: `${STACK_NAME}`


## 2. Backend-only stack

**Path:** `deployment/docker/backend`

- Image: `Agit8or/Depl0y-backend`
- Runs **only uvicorn** (no nginx) – equivalent to the `depl0y-backend` systemd service from the installer.
- Intended to sit **behind a reverse proxy** (nginx, Traefik, load balancer, etc.).

**Start:**

```bash
cd deployment/docker/backend
docker compose up -d
```

By default the compose file exposes:

- Host port `8081` → container port `8080` (the backend HTTP port).

You should place your own reverse proxy in front of this if you use the backend-only image.


## 3. Frontend-only stack

**Path:** `deployment/docker/frontend`

- Image: `Agit8or/Depl0y-frontend`
- Runs **nginx only**, serving the SPA and proxying `/api` to the backend.
- Designed to be paired with the backend stack or any other reachable backend.

**Start:**

```bash
cd deployment/docker/frontend
docker compose up -d
```

By default the compose file exposes:

- Host port `8080` → container port `80` (nginx).

### Configuring the backend URL

The frontend nginx config uses a templated `BACKEND_BASEURL`:

- Template file: `deployment/docker/frontend/nginx.conf`
- In the image it is installed as `/etc/nginx/templates/default.conf.template`.
- On container start, nginx's entrypoint replaces `$BACKEND_BASEURL` with the environment value.

Relevant snippet:

```nginx
location /api {
    proxy_pass $BACKEND_BASEURL;
    # standard proxy headers and timeouts
}
```

In the frontend stack:

- `.env.example` defines a default:
  - `BACKEND_BASEURL=http://backend:8000`
- `docker-compose.yml` wires it into the container:

```yaml
environment:
  BACKEND_BASEURL: '${BACKEND_BASEURL:-http://backend:8000}'
```

You **must** set `BACKEND_BASEURL` to a URL that is reachable from the frontend container, for example:

- `http://backend:8000` – if `backend` is a Docker DNS name on a shared network.
- `http://depl0y-backend.internal:8080` – if you front the backend with an internal load balancer.


## 4. Versioning and admin credentials

### Dynamic version tags

All build scripts (`build-and-push.sh` under each stack) generate versions in the form:

- `yyyy.mm.dd.hhmm` (e.g. `2025.11.19.1530`)

Each build:

- Tags the image as `:<timestamp>` **and** as `:latest`.
- Injects the same value into the container as `APP_VERSION`.
- `init_system_settings.py` persists this into the DB `system_settings` table.

### Admin user

Admin credentials are controlled via environment variables consumed by `init_admin_user.py`:

- `ADMIN_USERNAME` (default `admin`)
- `ADMIN_PASSWORD` (default `admin`)

These are wired in the backend/combined compose files via `environment:` blocks.


## 5. Data persistence and bind mounts

All stacks follow the same pattern for data persistence:

- Bind mounts rooted at `/custom/docker/stacks` by default
- Stack name is controlled via `STACK_NAME`.

You can safely upgrade containers (including watchtower-based updates) without losing data, as the database and other state live in the bind-mounted volumes, not inside the container filesystem.

