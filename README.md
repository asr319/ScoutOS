# ScoutOS

This repository contains the code and server setup script for deploying ScoutOS.

To provision a new server, run the `setup_scoutos_server.sh` script on your Ubuntu-based host. The script installs Docker, clones this repository, configures Nginx with SSL, and sets up monitoring via Prometheus Node Exporter.

The `ScoutOS` folder now contains a FastAPI backend with a Docker-based deployment setup. Run `docker-compose up` inside that directory to start the development stack.

For information on how to report security issues, see [SECURITY.md](SECURITY.md).
