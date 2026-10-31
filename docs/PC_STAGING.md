# Windows PC staging and restore drill

Decision: use the operator's PC as the first isolated staging and **restore** instance. This proves local recovery without paying for a second host. It does NOT validate PebbleHost's Java runtime, public Bedrock networking or production throughput.

## Prerequisites

1. Install a trusted, supported Java 25 runtime on the Windows PC; record `java -version` verbatim in a private operations note. The old environment was Java 17, so no local server launch has been demonstrated.
2. Clone the review branch and run `python scripts/manage.py validate`, unit tests, `download`, `package` and `verify-package` from the README.
3. The operator must review Minecraft's EULA and explicitly agree to it before first boot. Never check `eula.txt` into Git.
4. Use a separate, empty local directory outside the repository for stage world, plugin state, generated configs and all keys; never use an existing world directory. Bind test services to loopback/LAN only; do not open router ports. Use a different Java TCP and Bedrock TCP+UDP port, confirming neither is occupied.
5. Use the manual initial-install/first-boot sequence from DEPLOYMENT to capture real generated defaults; do not treat synthetic fixtures as defaults. Keep the test whitelist on and Java online authentication enabled. Internet sign-in may still be required by clients.

## Prove real restore

1. Have one Java and one Bedrock tester join locally/LAN, perform identifiable actions and document inventories, coordinates and world markers privately.
2. Type `stop` in the local console, wait for saves and process exit. Copy the **entire server root** into `private/stopped-copy` (not the tracked repository).
3. From the repo run `python scripts/manage.py backup private/stopped-copy backups/local-drill-UNIQUE --confirmed-stopped`, then `verify-backup`, then `restore backups/local-drill-UNIQUE private/restore-drill-UNIQUE`. Use new paths each time; the tools refuse existing outputs.
4. Launch the restored copy as a distinct instance with test-only ports. Keep original server stopped, or ensure the two servers cannot share the same account, world path or network listeners. Test both users, plugin state, Floodgate identities, Nether/End, CoreProtect database if enabled, a clean restart, and operator restrictions.
5. Log Java build, ports, software lock SHA, backup hash, shutdown proof, player test results and elapsed recovery time in a redacted copy of `docs/results/TEMPLATE.md`. Keep raw player IDs, inventory detail and credentials off Git.
6. Do not connect a restored stage instance to a live production identity endpoint without deliberate network and privacy controls.

A local test PASS is **not** a hosted restore PASS. After host purchase, repeat one recovery exercise using an exported complete Premium backup to an isolated instance (PC is acceptable for testing byte/data recovery, but host-specific disaster recovery remains separate).
