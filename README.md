# ScoutOS

This repository contains the code and server setup script for deploying ScoutOS.

To provision a new server, run the `setup_scoutos_server.sh` script on your Ubuntu-based host. The script installs Docker, clones this repository, configures Nginx with SSL, and sets up monitoring via Prometheus Node Exporter.

## Configuring setup variables

Before running the server setup script, open `setup_scoutos_server.sh` and adjust the values defined near the top of the file. Variables like `REPO_URL`, `DOMAIN` and `EMAIL` should be customized to match your environment. For automated deployments, an identical script is available at `ScoutOS/scripts/setup_scoutos_server.sh`.

The `ScoutOS` folder now contains a FastAPI backend with a Docker-based deployment setup. Run `docker-compose up` inside that directory to start the development stack.
An additional example project lives in the `scoutos/` directory with a similar layout and a helper script for automated deployments.

The stack now includes a React dashboard served from the `frontend` container. Visit `http://localhost:3000` after running Docker Compose to see live metrics update over WebSockets.
You can also experiment with the AI chat interface at `/chat.html` which connects to the backend AI API. The chat page sends JSON `{"prompt": "text"}` to `/api/ai/prompt` and displays the `response` field from the server.

The backend now exposes an AI API at `/api/ai/prompt`. Each request persists the prompt and generated response in a local SQLite database so the agent can recall prior interactions.

There are also endpoints for storing long-lived notes. POST JSON `{ "topic": "label", "content": "text", "summary": "optional" }` to `/api/memory` to persist a memory entry. Retrieve all entries for a topic via `GET /api/memory/{topic}`.

## Backend configuration

Set a strong `SECRET_KEY` environment variable before starting the backend. If this variable isn't defined, the app defaults to a testing key which should not be used in production.

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
Dependabot now monitors dependencies in `ScoutOS/backend` and `ScoutOS/frontend`.
Our CodeQL workflow scans both the Python backend and GitHub Actions workflows to catch issues early.

## GitHub Pages

The `docs/` directory contains the homepage used for GitHub Pages. To publish it:

1. Create a branch named `live_update` from your default branch if it doesn't exist.
2. Open repository **Settings** > **Pages**.
3. Select the `live_update` branch and `/docs` as the folder.
4. Enable **Enforce HTTPS** for secure connections.
5. Keep the repository private so only authorized collaborators can view the site.
6. Protect the `live_update` branch to restrict updates.

Once saved, GitHub Pages will serve `docs/index.md` from that branch.
