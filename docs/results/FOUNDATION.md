# Foundation validation — 2026-10-30

Status: PASS for the checks below; **not a gameplay-readiness result**.

Environment: Linux, Python 3.12, PyYAML 6.0.3. Java 17 present but unused; no
server execution, EULA acceptance, host purchase or world creation occurred.

| Executed check | Result |
| --- | --- |
| Lock/policy/workflow validation | PASS |
| Python safety test suite | PASS, 26 tests |
| Official artifact downloads | PASS, Paper 55,258,607 bytes; Geyser 52,115,333; Floodgate 11,561,096 |
| SHA-256 against official metadata | PASS for all three JARs; exact hashes in versions.lock.json |
| JAR archive integrity / expected descriptors | PASS |
| Pinned download cache reuse | PASS; no fresh-version selection |
| Real binary package creation and exact-manifest verification | PASS |
| Synthetic backup and restore | PASS, byte-identical, including synthetic secret/player-file stand-ins |
| Initial configuration rendering | PASS on synthetic fixtures only; actual generated defaults BLOCKED |
| Existing-target protection / tampering / malformed download cases | PASS in safety suite |
| Tracked-file guard and staged whitespace check | PASS |

UPDATE (2026-10-30): Earlier GitHub Actions check for foundation commit
`0271daa` completed successfully (including configured OS matrix and binary
package jobs). Amendment head `834aa4a` subsequently passed GitHub Actions on Linux, Windows, and the pinned-artifact packaging job. The full unit test suite at that commit passed **32 synthetic safety tests** (26 foundation tests plus 6 plugin-update tests). Re-check new documentation changes before squash merging.

NOT RUN at initial local validation (later GitHub CI performed Windows/Linux Python checks; no server boot): host deployment, Java 25 runtime,
actual Paper-generated config capture, real Java/Bedrock joins, gameplay,
restart persistence, actual world recovery, live upgrade/rollback and 5/10/20
active-player load tests. Missing hosting access, legal acceptance, runtime,
allocated ports and testers are recorded in HANDOFF.

The deployment manifest explicitly lists `server.jar`, the two plugin JARs and
`versions.lock.json`, with size and SHA-256 for each. `manifest.json` describes
those payload files and is not self-hashed. No worlds, keys, permissions,
credentials or operator configs are inside the package.
