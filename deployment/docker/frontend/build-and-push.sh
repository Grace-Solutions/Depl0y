#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-Agit8or/Depl0y-frontend}"
APP_VERSION="${APP_VERSION:-$(date +%Y.%m.%d.%H%M)}"
VERSION_TAG="${IMAGE_TAG:-${APP_VERSION}}"

echo "Building ${IMAGE_NAME}:${VERSION_TAG} and ${IMAGE_NAME}:latest from ${ROOT_DIR}..."
docker build \
  -f "${ROOT_DIR}/deployment/docker/frontend/Dockerfile" \
  --build-arg APP_VERSION="${VERSION_TAG}" \
  -t "${IMAGE_NAME}:${VERSION_TAG}" \
  -t "${IMAGE_NAME}:latest" \
  "${ROOT_DIR}"

if [ "${PUSH:-false}" = "true" ]; then
  echo "Pushing ${IMAGE_NAME}:${VERSION_TAG} and ${IMAGE_NAME}:latest..."
  docker push "${IMAGE_NAME}:${VERSION_TAG}"
  docker.push "${IMAGE_NAME}:latest"
fi

echo "Done."

