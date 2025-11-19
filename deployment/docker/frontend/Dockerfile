FROM nginx:alpine

ARG APP_VERSION=1.1.9

ENV APP_VERSION=${APP_VERSION}

# Copy built frontend assets into nginx web root
COPY src/frontend/dist /usr/share/nginx/html

# Custom nginx config for SPA routing (serve index.html for unknown routes)
COPY deployment/docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

