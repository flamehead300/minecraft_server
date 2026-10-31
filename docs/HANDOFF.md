# Handoff — 2026-10-30

## Current state

Repository: https://github.com/flamehead300/minecraft_server.
Do not hard-code repository visibility; inspect GitHub settings before sharing access.
The user created this repository and authorized it as the destination. Inspection
confirmed it was empty with no branches, files or AGENTS.md. Initialized `main`
with a minimal README, then created `feat/crossplay-foundation` for review.
PR #1 was squash-merged into `main` as `43202b9` after CI passed;
browser or Google sign-in is not required. No existing remote work was overwritten.

The original local preparation history ends at 1926fde; the remote review branch
uses the new repository's initial commit as its parent. Use the remote branch
for future work. Prior downloadable archives are pre-publication snapshots.

## Decisions

- PebbleHost Premium 8 GB, approximately $18/month planning estimate; final price,
  location and extras must be verified by operator before purchase.
- Paper 26.3 build 231, Geyser-Spigot 2.12.1 build 1279, Floodgate-Spigot 2.2.5
  build 141. Exact URLs/hashes in lock; actual JARs checked against official hashes.
- Java 25 required. Exact managed runtime unverified. Workspace has Java 17.
- Current NetherNet mode requires separate Bedrock TCP+UDP port; do not use
  historical same-port UDP advice without reviewing the selected transport.
- Survival/normal, whitelist, Java authentication, Floodgate, view 8 / simulation 6.
- Initial heap proposal 2–6 GiB; measure total memory under the 8 GB cap.
- Manual panel/file transfer only. No host purchase, EULA acceptance or world overwrite.
- Provisional weekly manual clean-stopped backups plus pre-change backups, with up to seven days (or more when missed) lost progress. Operator acceptance pending; encrypted off-host copies and isolated PC restore required.

## Milestones and evidence

| Milestone | State |
| --- | --- |
| Workspace/instruction inspection | Complete; empty workspace, new isolated Git repository. |
| Official documentation / version selection | Complete at documentation level; host-specific confirmations listed in VERIFICATION. |
| Real JAR downloads / SHA-256 | All three match official release metadata; archive validation passed. |
| Repository automation and package | Implemented; see results/FOUNDATION.md for final executed checks. |
| Actual generated defaults | BLOCKED: Java 25 + operator-authorized first boot/EULA required. Renderer refuses absent/unmatched defaults. |
| Remote GitHub branch / PR / Actions | Draft PR #1 has 32 passing synthetic tests and GitHub Actions passed at `834aa4a`; final documentation changes require new checks before squash merge. |
| One Java + one Bedrock, restart, actual restore | BLOCKED: hosting/allocated ports, operator EULA step, both clients and testers. Not passed. |
| 5/10/20-player capacity | NOT RUN; needs real or representative active workloads plus mixed real clients. |
| Live update and rollback | NOT RUN; requires real baseline snapshot and staged candidate. |

## Amendments — 2026-10-30

- **Host pre-sales:** `docs/HOST_PRESALES.md` records $18/month advertised for Premium 8 GB, published SFTP, Premium backups and scheduling. A support reply confirming Java 25, separate NetherNet TCP+UDP port and schedule-backup capability is **not received**; purchase gate stays closed.
- **PC staging:** Accepted. `docs/PC_STAGING.md` uses operator Windows PC for first full restore and Java+Bedrock crossplay drill, plus explicit local Java 25 prerequisite. Real local launch remains NOT RUN.
- **Scheduled stop → backup → start:** Accepted as a target, **not enabled**. PebbleHost lists only power/console task actions; no verified backup task or completion barrier. Use manually supervised stopped backups until host confirms a supported transactional sequence. Do not implement stop → fixed timer → start as though reliable.
- **Plugin-only fast path:** Added `scripts/plugin_update.py`, `tests/test_plugin_update.py` and `docs/PLUGIN_UPDATES.md`. Requires unchanged Paper and Java lock plus full stopped backup and stage tests. At head `834aa4a`, GitHub Actions on Windows, Linux, and package validation passed.
- **CoreProtect:** Requested. See `docs/COREPROTECT.md`; public v24.1 documented through MC 26.2, whereas a 26.3-compatible 25.1 release is listed via Patreon without a verified download/hash. **Do not silently deploy a nonmatching or floating build**. Pin, package and test when eligible verified artifact is obtained.
- **Visibility wording:** Removed fixed '(private)' labels from HANDOFF and PUBLISH. Verify GitHub settings rather than assuming access.

## Correction and review — 2026-10-30

- Corrected BACKUP_RESTORE.md: the previous daily manually stopped schedule
  and 24-hour RPO were unrealistic without confirmed automation. The provisional
  baseline is a weekly manually stopped full off-host snapshot, plus an extra
  backup before every risky change. It retains four verified weekly copies,
  three month-end copies, and pre-upgrade copies. **Up to seven days or more of
  progress may be lost.** The owner has not yet accepted this cadence; do not
  claim the policy is running or open production without operator sign-off.
- On `834aa4a`: 32 local safety tests passed, Linux/Windows GitHub Actions
  and artifact checks passed. The final PR-head CI passed before squash merge into `main`.
- PR #1 was squash-merged; `main` is now authoritative. The previous feature
  branch and pre-publication archives are historical.
- Official CoreProtect CE v24.1 supports Minecraft through 26.2, not 26.3.
  It is optional for the whitelisted first milestone; do not install it
  until a verified supported release is pinned.
- GitHub repository visibility was verified as public during this review.
  Keep private game/server data, credentials and private plugin keys out of Git.

## Exact next steps

1. Obtain a written PebbleHost reply using HOST_PRESALES.md. Confirm Java 25,
   dual-protocol Bedrock port, SFTP and reliable backup procedure. No purchase yet.
2. Use PC_STAGING.md to prove one Java + Bedrock join, restart persistence and
   full stopped backup/restore after operator-approved EULA acceptance.
3. Continue work on `main`, which contains the squash merge `43202b9`. Confirm its current SHA and CI before changing deployment tooling; CI alone is not evidence of game readiness.
4. Obtain the operator's explicit acceptance of the weekly backup cadence and potential seven-day data loss (or select a verified alternative). Only after host purchase and operator EULA approval, follow DEPLOYMENT.md
   initial-install steps and capture actual generated defaults.
5. Execute TEST_PLAN milestone 1 against the actual host, then stage 5/10/20
   active-player capacity tests with representative workloads.
6. Obtain a compatible immutable CoreProtect release and verified hash,
   extend the binary lock and manifest, test it on PC, then approve installation.

## Continuation prompt

> Open `flamehead300/minecraft_server` on `main`. Confirm PR #1 was
> squash-merged in commit `43202b9` and verify the current branch/SHA.
> Read `docs/HANDOFF.md`, `docs/HOST_PRESALES.md`,
> `docs/BACKUP_RESTORE.md` and relevant AGENTS.md instructions. Confirm
> owner acceptance of the provisional weekly off-host backup policy or a
> demonstrated automatic alternative before production. Continue the
> first unchecked milestone: one Java and one Bedrock player together,
> restart persistence and a real restore drill. Do not buy hosting,
> accept agreements, leak player data or overwrite a world. Record
> evidence honestly and update HANDOFF after each milestone.

The Git repository is the continuation record. Use
`python scripts/continuation.py` on `main` to print a prompt with the
current commit and this handoff, and forward its output to another chat.
