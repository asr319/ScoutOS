# ScoutOS

This repository contains the code and server setup script for deploying ScoutOS.

To provision a new server, run the `setup_scoutos_server.sh` script on your Ubuntu-based host. The script installs Docker, clones this repository, configures Nginx with SSL, and sets up monitoring via Prometheus Node Exporter.

The `ScoutOS` folder now contains a FastAPI backend with a Docker-based deployment setup. Run `docker-compose up` inside that directory to start the development stack.

The stack now includes a React dashboard served from the `frontend` container. Visit `http://localhost:3000` after running Docker Compose to see live metrics update over WebSockets.

For details on how to report vulnerabilities, see [SECURITY.md](SECURITY.md). Our workflow is to accept reports via email or GitHub's security advisories. The listed address is `security@example.com` as a placeholder—replace it with the real project contact.

## Setting up a self-hosted GitHub Actions runner

To run CI workflows on your own server, download the x64 runner package instead of the ARM64 build. The basic steps are:

```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.325.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.325.0/actions-runner-linux-x64-2.325.0.tar.gz
tar xzf actions-runner-linux-x64-2.325.0.tar.gz
RUNNER_ALLOW_RUNASROOT=1 ./config.sh --url https://github.com/asr319/ScoutOS --token <TOKEN>
./run.sh
```

Replace `<TOKEN>` with the registration token from your repository settings.

## Development Notes

The backend code now follows basic `flake8` conventions for improved readability.
The Docker build workflow now points to `ScoutOS/backend/Dockerfile`.

## GitHub Pages

The `docs/` directory contains the homepage used for GitHub Pages. To publish it:

1. Open repository **Settings** > **Pages**.
2. Select the `live_update` branch and `/docs` as the folder.
3. Enable **Enforce HTTPS** for secure connections.
4. Keep the repository private so only authorized collaborators can view the site.
5. Protect the `live_update` branch to restrict updates.

Once saved, GitHub Pages will serve `docs/index.md` from that branch.
