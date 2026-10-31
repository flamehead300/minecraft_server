# GitHub publication and handoff

Repository: https://github.com/flamehead300/minecraft_server
Visibility verified **public** on 2026-10-30; check account settings before
sharing later. Do not commit secrets, worlds, player data or plugin databases.

PR #1 from `feat/crossplay-foundation` was **squash-merged** into `main`
as commit `43202b9feaf9765684a231341493b2e06b462dd8`, after the final
GitHub Actions workflow (Linux, Windows, artifact verification) passed.
The review branch, its per-file commit history and pre-publication ZIPs are
historical. Do not force-push that history onto `main`.

Clone the authoritative repository into a new directory:

```text
git clone https://github.com/flamehead300/minecraft_server.git
cd minecraft_server
git switch main
git status
git log -1 --oneline
```

For follow-up work, branch from the **current `main`** and open a new PR.
Host deployment is manual and separate from a source merge; nothing is live
or hosting-purchased. Read HANDOFF.md, HOST_PRESALES.md, BACKUP_RESTORE.md
(provisional weekly manual policy awaiting owner acceptance), PC_STAGING.md,
PLUGIN_UPDATES.md and COREPROTECT.md before proceeding.
