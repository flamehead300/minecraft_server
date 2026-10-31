# Handoff — 2026-10-30

## Current state

Repository: https://github.com/flamehead300/minecraft_server (private).
The user created this repository and authorized it as the destination. Inspection
confirmed it was empty with no branches, files or AGENTS.md. Initialized `main`
with a minimal README, then created `feat/crossplay-foundation` for review.
The implementation is being published through the GitHub connector; browser or
Google sign-in is not required. No existing remote work was overwritten.

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
| Remote GitHub branch / PR / Actions | Review branch created; publication and CI results recorded below as they complete. |
| One Java + one Bedrock, restart, actual restore | BLOCKED: hosting/allocated ports, operator EULA step, both clients and testers. Not passed. |
| 5/10/20-player capacity | NOT RUN; needs real or representative active workloads plus mixed real clients. |
| Live update and rollback | NOT RUN; requires real baseline snapshot and staged candidate. |

## Exact next steps

1. Review the pull request on `flamehead300/minecraft_server`, branch
   `feat/crossplay-foundation`. Check its latest commit and GitHub checks before
   merging. Do not deploy merely because repository checks pass.
2. Confirm host price, Java 25 exact runtime, separate TCP+UDP Bedrock allocation,
   secure transfer and backup capabilities. Do not buy or agree to terms on the
   user's behalf.
3. After the operator provisions the service and accepts agreements, follow
   DEPLOYMENT initial-install steps. Generate/capture defaults and review initial
   config proposals before exposing the whitelisted listener.
4. Execute TEST_PLAN gate 1: one real Java + one real Bedrock player, restart
   persistence, then complete stopped backup/restoration into a separate instance.
   Record evidence and update this file. Only then start capacity stages.

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
