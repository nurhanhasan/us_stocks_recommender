FROM n8nio/n8n

USER root

# Install dependencies
RUN apk update && apk add --no-cache \
    curl

# Install Docker CLI for Alpine.
RUN apk update && \
    apk add docker-cli
    
RUN rm -rf /var/cache/apk/*

# Create docker group if it doesn't exist and add node user.
# NOTE: Run `getent group docker` on the host to get docker group GID.
# This is to avoid different GID on the host and inside the container which causes permission error.
RUN addgroup -g 998 docker || true \
    && adduser node docker

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.40.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Set timezone to New York
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/America/New_York /etc/localtime \
    && echo "America/New_York" > /etc/timezone

USER node