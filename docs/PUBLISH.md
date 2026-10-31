# GitHub review workflow

Repository: https://github.com/flamehead300/minecraft_server.
Repository visibility is an account setting: verify it on GitHub before sharing a link.
Review branch: `feat/crossplay-foundation`; target: `main`.

The user created the empty repository. The GitHub connector initialized a minimal
README on main, then created the review branch. All implementation files are
submitted for review there. No browser or Google authentication is required.

Clone the authoritative repository into an unused directory:

```text
git clone https://github.com/flamehead300/minecraft_server.git
cd minecraft_server
git switch feat/crossplay-foundation
git status
git log -1 --oneline
```

Inspect the pull request and GitHub checks before merging. The original source
ZIP and Git bundle are pre-publication snapshots with a separate local history;
do not force-push that history over this repository. Use the remote review branch
for continuation. Host deployment remains manual and separate from merging.
See HOST_PRESALES.md before purchase, PC_STAGING.md for the restore drill,
PLUGIN_UPDATES.md for a safe plugin-only fast path, and COREPROTECT.md for
the planned anti-grief plugin compatibility gate.
