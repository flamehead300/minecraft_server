# Backups, restoration and rollback

**No real Minecraft recovery has passed yet.** The operator's Windows PC is\nthe initial isolated restore destination; see `docs/PC_STAGING.md`. Automated tests verify byte-copy
integrity with synthetic fixtures. A running restored world with both client
types is a separate required acceptance test.

## Reliable initial procedure

1. Announce downtime. Disable scheduled restarts for the window. Send `stop` in
   the panel console. Wait for completed saves and process offline. A crash or
   Kill is not a confirmed clean shutdown. Do not restart until copying finishes.
2. Use supported encrypted transfer or a panel full-backup download to copy the
   **entire stopped server root** to `private/stopped-copy/` on the operator PC.
   Preserve all worlds/dimensions, region/entity/POI files, playerdata, advancements,
   statistics, ops/whitelist/bans, all configs, plugins and plugin databases,
   Floodgate key and linking data, software JARs and `versions.lock.json`.
   Export separately any external database if later plugins introduce one.
3. Store a private operations note alongside that copy: clean shutdown time,
   Minecraft version, repository commit, full Java vendor/patch/build, startup
   flags, heap, port allocations, world folder names and responsible operator.
   Save logs proving clean shutdown privately. Never include host credentials.
4. Create and validate a snapshot outside the source:

```text
python scripts/manage.py backup private/stopped-copy backups/2026-10-30-before-update --confirmed-stopped
python scripts/manage.py verify-backup backups/2026-10-30-before-update
python scripts/manage.py restore backups/2026-10-30-before-update private/restore-drill
```

Use a new timestamped destination each time. Commands refuse existing targets,
symlinks, nested backup destinations and hash mismatches. The backup command
compares the source before and after copying to detect changes. It cannot verify
remote process state or detect data omitted during the earlier host download:
the operator must inspect the remote inventory and clean shutdown log. Hashes
detect corruption, not Minecraft consistency or malicious substitution.

5. Encrypt the snapshot and manifest together using your trusted backup tool,
   upload to a private off-host destination, then download/decrypt and verify it.
   The Python tool does **not encrypt**; `backups/` contains secrets. Use an
   encrypted local disk, restricted access and private storage. Never attach it
   to GitHub, a public download or an AI chat. Keep decryption recovery material
   separately. Host login credentials belong in a password manager, not backups.

## Retention and schedule

Initial policy: one clean stopped snapshot daily in an agreed maintenance window;
retain 7 daily, 4 weekly and 3 monthly recovery points plus every pre-upgrade
snapshot for at least 30 days. Keep at least one proven previous release until
the next release passes. Maintain two off-host copies, one separate from the
primary computer. Retention pruning is manual and only after a newer copy is
verified. Check storage capacity and alert on failed/missed backups.

Target recovery point loss: no more than 24 hours in the initial daily schedule.
Target recovery time: 60 minutes, **unmeasured** until the drill. Agree on a
maintenance time with players before enabling any panel schedule. Premium's
advertised daily/hourly backups supplement this process; their application
consistency and effective retention need confirmation. No live backup is approved
until save coordination, files/databases and restore consistency are demonstrated.

## Restoration drill

Restore to a separate empty instance, with distinct ports and no public routing.\nFor the first drill use the PC as the destination; this does not prove hosted\nprovisioning, recovery timing or DDoS/network behavior. See PC_STAGING.md.
Use the saved Java runtime and complete matching software/config/data snapshot.
Adjust only test-instance ports/bind address; record those diffs separately.
Start with whitelist on. Confirm both Java and Bedrock identities, inventories,
ender chests, XP, beds, builds, entities and progress in all dimensions. Confirm
ops restrictions and that Floodgate identities did not change. Restart and repeat.
Measure elapsed download/decrypt/upload/start/rejoin time and record actual RTO.

For the first drill, place identifiable blocks/chests in each visited dimension,
record inventories/XP/coordinates privately, stop and back up, restore, and verify
those exact markers. Do not claim recovery solely because the ZIP opens or hashes
match. Repeat monthly and before upgrades; keep redacted results in docs/results.

Rollback is this complete restoration process using the pre-update snapshot.
Replacing only a JAR is not rollback after a world format change. Never point the
old server at the upgraded world. No script here overwrites an existing world.
