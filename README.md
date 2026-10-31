# Minecraft survival crossplay server

Target: **20 active Java + Bedrock players total**, ordinary survival on PebbleHost
Premium 8 GB. Capacity is a test target, not a promise. Budget: approximately
US$18/month before extras; exact checkout price still requires confirmation.

**Status: foundation built, not live-ready.** No hosting purchased, no legal
agreements accepted, no world created or overwritten. Read [HANDOFF](docs/HANDOFF.md)
for verified results and blockers. First milestone: one Java player and one
Bedrock player together, progress retained after restart, successful restore to
a separate instance.

| Component | Pin |
| --- | --- |
| Minecraft / Paper | 26.3 / build 231 |
| Java runtime | Java 25 required; exact host vendor/patch/build pending |
| Geyser-Spigot | 2.12.1 build 1279 (JAR descriptor says SNAPSHOT) |
| Floodgate-Spigot | 2.2.5 build 141 (JAR descriptor says SNAPSHOT) |

Exact official URLs and SHA-256 values are in `versions.lock.json`. No ViaVersion
is needed for the documented Java 26.3 target; do not add extra plugins casually.
Bedrock compatibility is documented as 26.40–26.60; real client checks are pending.
Bedrock updates can force a new reviewed Geyser release even with a pinned server.

## Prepare locally

Python 3.11+ is required on the operator's computer. These commands work in
PowerShell or a shell with `python` available. No Python, SSH, Docker or root
access is required on PebbleHost.

```text
python -m pip install -r requirements.txt
python scripts/manage.py validate
python -m unittest discover -s tests -v
python scripts/manage.py download
python scripts/manage.py package dist/release-26.3-231
python scripts/manage.py verify-package dist/release-26.3-231
```

Existing package destinations are refused. Re-running downloads verifies and
reuses matching files; mismatches fail. Packages contain only three JARs, the
version record and a hash manifest. Keep the whole package for review; upload
only the three JARs and version record to the server. See
[DEPLOYMENT](docs/DEPLOYMENT.md) for the initial configuration and upgrade paths.
The supplied source archive is **not** a server-root deployment archive.

## Connect as a player

Ask the operator for the actual address and ports; defaults such as 25565 and
19132 are not allocations.

| Client | Instructions |
| --- | --- |
| Java | Install Minecraft Java 26.3, sign into your licensed account, Multiplayer → Add Server → `HOST:JAVA_PORT`. Ask to be whitelisted. |
| Bedrock mobile / Windows | Use a supported release, sign into Microsoft/Xbox, Play → Servers → Add Server. Enter `HOST` and the separately allocated `BEDROCK_PORT`. Ask to whitelist your exact Xbox gamertag. Floodgate does not require a separate Java purchase. |
| Xbox / PlayStation / Switch | Direct custom-server entry is not universally available. The [Geyser console guide](https://geysermc.org/wiki/geyser/using-geyser-with-consoles/) describes third-party workarounds. Compatibility, account restrictions, subscriptions and network requirements must be checked per device; console access is not an acceptance claim here. |

Java accounts remain authenticated (`online-mode=true`). Geyser uses Floodgate
authentication; never solve a join problem by switching the server to offline mode.
The selected NetherNet mode uses a separate Bedrock TCP+UDP port. Keep testing
whitelisted until all acceptance gates pass.

## Requested amendments and limits

- Before purchase, use [HOST_PRESALES](docs/HOST_PRESALES.md). Java 25 and the dual TCP+UDP Bedrock allocation still need written confirmation.
- Run the first stage and restore drill on the operator's [Windows PC](docs/PC_STAGING.md).
- Stop → backup → start automation is **not enabled**: PebbleHost's published scheduler documents power/console actions but not an awaited backup step. Continue supervised stopped backups.
- For Geyser/Floodgate-only releases, use [PLUGIN_UPDATES](docs/PLUGIN_UPDATES.md) and the fail-closed `scripts/plugin_update.py` package helper. This does not change Paper or world data.
- [CoreProtect](docs/COREPROTECT.md) is **planned but NOT packaged or verified** until an official 26.3-compatible build/hash is approved. Do not use floating latest downloads.

Plugin-only candidate example, after saving the current lock and independently preparing a new, pinned full candidate package:

```text
python scripts/plugin_update.py package private/old-versions.lock.json dist/candidate-full dist/plugin-update-candidate
python scripts/plugin_update.py verify private/old-versions.lock.json dist/plugin-update-candidate
```

These are **staging-only** files. Do not upload `server.jar` from a plugin-only candidate. Back up and test first.

## Operations

- [Configuration policy](config/README.md): defaults provenance, ports, gameplay effects.
- [Deployment and upgrades](docs/DEPLOYMENT.md): manual game-panel workflow.
- [Backups and recovery](docs/BACKUP_RESTORE.md): provisional weekly manual stopped backups plus pre-change backups, with up to seven days (or more if missed) of potential progress loss. Owner approval required before launch.
- [Test plan](docs/TEST_PLAN.md): functional milestone, 5/10/20-player performance gates.
- [Verification sources](docs/VERIFICATION.md): official documentation and remaining host checks.
- [Pre-purchase inquiry](docs/HOST_PRESALES.md): vendor checklist and unanswered questions.
- [Local recovery staging](docs/PC_STAGING.md): Windows PC restore drill.
- [Plugin-only updates](docs/PLUGIN_UPDATES.md): limited JAR replacement, no server upgrade.
- [CoreProtect gate](docs/COREPROTECT.md): anti-grief plugin plan and version blocker.

For a new chat: **Read `docs/HANDOFF.md` on `feat/crossplay-foundation`, verify the
current branch and commit, and continue the next unchecked milestone. Do not
purchase hosting, accept agreements, or overwrite an existing world.**
