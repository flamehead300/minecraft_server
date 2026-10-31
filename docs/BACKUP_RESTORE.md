# Backups, restoration and rollback

**No real Minecraft recovery has passed yet.** The operator's Windows PC is
the initial isolated restore destination; see `docs/PC_STAGING.md`. Automated tests verify byte-copy
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

### Provisional manual policy — operator acceptance required

**Proposed cadence:** one **clean stopped full backup weekly**, and an additional
verified stopped backup **before each update, configuration change, migration,
plugin installation, or other potentially destructive operation**. This is a
proposed minimum, not an assertion the owner has committed to it or that any
backup has happened. Agree on a specific weekly maintenance window before
opening the server. If a weekly manual cadence is not practical, obtain and
restore-test a reliable managed/automatic alternative first.

Each backup requires confirmed clean shutdown, a complete server-root copy
(including all plugin databases, world data, keys and permission files),
SHA-256 verification, encryption, and at least one independent copy **outside
the running host and the operator PC**. Prefer two independent encrypted storage
locations. Keep a private operator log recording date/time, archive/checksum,
off-host location, verification result and responsible person. The backup script
does not encrypt. Do not commit secrets, database records or this log.

**Off-host retention target:** keep 4 verified weekly snapshots, 3 month-end
snapshots (a week-ending point may also be month-end), plus pre-upgrade snapshots
for at least 30 days. Keep the old complete release until the new release has
passed a real restore. Prune only after newer copies are verified; check storage
capacity. Premium's advertised four manual panel slots and short retention are
supplementary and cannot meet this off-host policy alone.

**Recovery point exposure:** successful weekly backups may still lose **up to
seven days of player/world progress** if the server is lost. If a backup is
missed, corrupted, or never exported off-host, possible loss may exceed a week.
The former **24-hour RPO target is withdrawn** unless a daily or more frequent
backup method is actually verified. Pre-change backups do not substitute for
routine protection.

**Recovery time target:** 60 minutes remains **unmeasured**, not a guarantee.
Document download/decrypt/upload/start/rejoin time in the PC restore drill and
repeat the drill with the selected host.

**Unattended scheduling is NOT authorized:** PebbleHost's published Scheduled
Tasks guide lists Power Action and Send Command; offsets are fixed delays, not
checks that save/shutdown or backup completed. Until the host confirms a native
or supported backup action with reliable completion and failure handling, use
an operator-supervised stop → verify fully offline → copy/hash/encrypt/export →
start procedure. Do not implement stop → fixed delay → backup → fixed delay →
start. See HOST_PRESALES.md questions 5 and 6.

## Restoration drill

Restore to a separate empty instance, with distinct ports and no public routing.
For the first drill use the PC as the destination; this does not prove hosted
provisioning, recovery timing or DDoS/network behavior. See PC_STAGING.md.
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
