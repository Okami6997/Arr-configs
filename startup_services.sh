#!/bin/bash
# Startup script for Tailscale, Docker, and Docker Compose

# Tailscale is already a system service, so we just ensure it connects
# Using sudo as tailscale up requires root privileges
sudo tailscale up

# Start Docker service (if not already started by systemd)
sudo systemctl start docker

# Start Docker Compose
# Change to your container directory
cd ~/docker_container || exit

# Restart containers
docker compose down
docker compose up -d
