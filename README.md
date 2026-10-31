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

## Operations

- [Configuration policy](config/README.md): defaults provenance, ports, gameplay effects.
- [Deployment and upgrades](docs/DEPLOYMENT.md): manual game-panel workflow.
- [Backups and recovery](docs/BACKUP_RESTORE.md): stopped-server snapshots and complete rollback.
- [Test plan](docs/TEST_PLAN.md): functional milestone, 5/10/20-player performance gates.
- [Verification sources](docs/VERIFICATION.md): official documentation and remaining host checks.

For a new chat: **Read `docs/HANDOFF.md` on `feat/crossplay-foundation`, verify the
current branch and commit, and continue the next unchecked milestone. Do not
purchase hosting, accept agreements, or overwrite an existing world.**
