FROM python:3.11-slim

ARG APP_VERSION=1.1.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION}

# System dependencies required by the backend (SSH, PDF, etc.)
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends \ 
       build-essential \ 
       curl \ 
       wget \ 
       sshpass \ 
       openssh-client \ 
       ca-certificates \ 
       libpango-1.0-0 \ 
       libpangocairo-1.0-0 \ 
       libgdk-pixbuf2.0-0 \ 
       libffi-dev \ 
       shared-mime-info \ 
    && rm -rf /var/lib/apt/lists/*

# Create application directories
RUN mkdir -p /opt/depl0y/backend \ 
    /opt/depl0y/frontend/dist \ 
    /var/lib/depl0y/db \ 
    /var/lib/depl0y/cloud-images \ 
    /var/lib/depl0y/isos \ 
    /var/lib/depl0y/ssh_keys \ 
    /var/lib/depl0y/cloud-init \ 
    /var/log/depl0y

WORKDIR /opt/depl0y/backend

# Install Python dependencies
COPY src/backend/requirements.txt /opt/depl0y/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt \ 
    && pip install --no-cache-dir weasyprint markdown requests

# Copy backend code and built frontend assets
COPY src/backend /opt/depl0y/backend
COPY src/frontend/dist /opt/depl0y/frontend/dist

# Default environment values (can be overridden at runtime)
ENV DATABASE_URL=sqlite:////var/lib/depl0y/db/depl0y.db \ 
    ISO_STORAGE_PATH=/var/lib/depl0y/isos \ 
    UPLOAD_DIR=/var/lib/depl0y \ 
    CLOUDINIT_TEMPLATE_PATH=/var/lib/depl0y/cloud-init \ 
    SSH_KEY_PATH=/var/lib/depl0y/ssh_keys \ 
    LOG_FILE=/var/log/depl0y/app.log \ 
    FRONTEND_DIST_PATH=/opt/depl0y/frontend/dist \ 
    APPLICATION_PORT_INTERNAL=8080

# Entrypoint script
COPY deployment/docker/combined/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

