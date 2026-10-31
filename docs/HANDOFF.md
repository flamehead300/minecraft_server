# Handoff — 2026-10-30

## Current state

Repository: https://github.com/flamehead300/minecraft_server.
Do not hard-code repository visibility; inspect GitHub settings before sharing access.
The user created this repository and authorized it as the destination. Inspection
confirmed it was empty with no branches, files or AGENTS.md. Initialized `main`
with a minimal README, then created `feat/crossplay-foundation` for review.
The foundation was published as draft PR #1 through the GitHub connector;
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
- Stopped full backups, encrypted off-host copies, restore into separate instances.

## Milestones and evidence

| Milestone | State |
| --- | --- |
| Workspace/instruction inspection | Complete; empty workspace, new isolated Git repository. |
| Official documentation / version selection | Complete at documentation level; host-specific confirmations listed in VERIFICATION. |
| Real JAR downloads / SHA-256 | All three match official release metadata; archive validation passed. |
| Repository automation and package | Implemented; see results/FOUNDATION.md for final executed checks. |
| Actual generated defaults | BLOCKED: Java 25 + operator-authorized first boot/EULA required. Renderer refuses absent/unmatched defaults. |
| Remote GitHub branch / PR / Actions | Draft PR #1 published; foundation validation previously passed. New amendment checks must be re-run. |
| One Java + one Bedrock, restart, actual restore | BLOCKED: hosting/allocated ports, operator EULA step, both clients and testers. Not passed. |
| 5/10/20-player capacity | NOT RUN; needs real or representative active workloads plus mixed real clients. |
| Live update and rollback | NOT RUN; requires real baseline snapshot and staged candidate. |

## Amendments — 2026-10-30

- **Host pre-sales:** `docs/HOST_PRESALES.md` records $18/month advertised for Premium 8 GB, published SFTP, Premium backups and scheduling. A support reply confirming Java 25, separate NetherNet TCP+UDP port and schedule-backup capability is **not received**; purchase gate stays closed.
- **PC staging:** Accepted. `docs/PC_STAGING.md` uses operator Windows PC for first full restore and Java+Bedrock crossplay drill, plus explicit local Java 25 prerequisite. Real local launch remains NOT RUN.
- **Scheduled stop → backup → start:** Accepted as a target, **not enabled**. PebbleHost lists only power/console task actions; no verified backup task or completion barrier. Use manually supervised stopped backups until host confirms a supported transactional sequence. Do not implement stop → fixed timer → start as though reliable.
- **Plugin-only fast path:** Added `scripts/plugin_update.py`, `tests/test_plugin_update.py` and `docs/PLUGIN_UPDATES.md`. Requires unchanged Paper and Java lock plus full stopped backup and stage tests. GitHub Actions needs verification on the new commit.
- **CoreProtect:** Requested. See `docs/COREPROTECT.md`; public v24.1 documented through MC 26.2, whereas a 26.3-compatible 25.1 release is listed via Patreon without a verified download/hash. **Do not silently deploy a nonmatching or floating build**. Pin, package and test when eligible verified artifact is obtained.
- **Visibility wording:** Removed fixed '(private)' labels from HANDOFF and PUBLISH. Verify GitHub settings rather than assuming access.

## Exact next steps

1. Obtain a written PebbleHost reply using HOST_PRESALES.md. Confirm Java 25,
   dual-protocol Bedrock port, SFTP and reliable backup procedure. No purchase yet.
2. Use PC_STAGING.md to prove one Java + Bedrock join, restart persistence and
   full stopped backup/restore after operator-approved EULA acceptance.
3. Review draft PR #1 on `feat/crossplay-foundation` and await passing GitHub
   checks on its newest commit before merging. Do not deploy on CI alone.
4. Only after host purchase and operator EULA approval, follow DEPLOYMENT.md
   initial-install steps and capture actual generated defaults.
5. Execute TEST_PLAN milestone 1 against the actual host, then stage 5/10/20
   active-player capacity tests with representative workloads.
6. Obtain a compatible immutable CoreProtect release and verified hash,
   extend the binary lock and manifest, test it on PC, then approve installation.

## Continuation prompt

> Open `flamehead300/minecraft_server`, verify the branch and commit and read
> `docs/HANDOFF.md`, `docs/results/FOUNDATION.md` and any AGENTS.md. Continue the
> first unchecked milestone on `feat/crossplay-foundation`. Preserve unrelated
> work. Do not purchase hosting, accept agreements or overwrite a world. Distinguish
> automated/synthetic checks from real crossplay, restart and restore tests. Update
> HANDOFF after each milestone and deliver a reviewable commit/PR.

The repository is the continuation record. Use `python scripts/continuation.py`
to print a current prompt with branch/commit and this handoff; forward that output
to the next chat. This avoids relying on conversational memory.
