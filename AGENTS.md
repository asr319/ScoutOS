# AGENT instructions

This repository uses a simple test workflow for shell scripts.

- When modifying any `*.sh` file, run `shellcheck` on that file before committing.
- Document significant changes in `README.md`.
- Keep commit messages short and descriptive.
- Mention in the `README` that `setup_scoutos_server.sh` includes variables such as
  `REPO_URL`, `DOMAIN`, and `EMAIL` that should be customized before running the script.
- When updating documentation, ensure `docs/index.md` links back to the repository
  `README` and briefly summarizes ScoutOS features.
- `SECURITY.md` should include a valid or clearly example security contact email.
