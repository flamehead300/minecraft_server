# PebbleHost deployment

## Before purchase or installation

No hosting purchase or EULA acceptance is authorized by this repository. The
operator must do those steps. Plan for Premium 8 GB, approximately $18/month
before extras. Confirm the actual monthly checkout total, taxes, location,
recurring fees and optional extras immediately before purchase. The public
pricing widget did not expose a definitive 8 GB quote during verification.

Public host documentation supports custom JARs, plugins, a game panel, file
transfer, additional ports and Premium backups. These are product-level claims,
not proof that the needed allocations exist on your instance. Before purchase,
confirm with the host or in the selected service:

- Java **25**, including vendor/full patch/build and whether it can be held
  stable or is host-updated. Save this in the private release record; update
  the lock's runtime record after verification. No exact host runtime is claimed yet.
- Custom Paper JAR and both Spigot plugins, with automatic JAR replacement disabled.
- A Java TCP allocation plus a **different** Bedrock allocation supporting
  **TCP and UDP** for NetherNet. Ask whether DDoS filtering passes both protocols.
  Additional-port availability alone is not confirmation of both protocols.
- The supported encrypted file-transfer method and host-key verification details.
  Prefer SFTP if provided; do not send credentials over unencrypted FTP.
- Downloadable complete backups, retention, disk limits and whether restores
  overwrite the entire instance. Our own stopped backup remains authoritative.
- Supported memory/startup controls, including a heap below 8 GB.

Use the host's panel and console. No root, SSH, systemd, Docker or deployment API
is assumed. The host lists an API article, but its permissions and deployment
semantics have not been verified. No automatic production deployment is included. Obtain a host response using\n`docs/HOST_PRESALES.md` before purchase.

## Initial installation (new world only)

1. Inspect the target in the panel. If any world or operator data exists, stop:
   use the upgrade/migration procedure. Do not run a reinstall wizard or delete
   files. Record assigned address, Java TCP port and Bedrock TCP+UDP port privately.
2. Build and verify the local package using README commands. Record repository
   commit and manifest SHA-256. Use panel maintenance/network restrictions so
   nobody can join during the first boot before whitelist settings exist.
3. In the stopped, empty instance, choose the host's **Custom JAR** option. Upload
   `server.jar`, `plugins/Geyser-Spigot.jar`, `plugins/floodgate-spigot.jar`, and
   `versions.lock.json` at precisely those relative paths. Match the configured
   startup JAR name to `server.jar`; verify current panel controls instead of
   assuming a historical UI label. Never select an auto-updating Paper installer.
4. Select confirmed Java 25 and supported heap settings (initial 2–6 GiB).
   Capture the effective command/runtime in the private release record.
5. The operator personally reviews and accepts Minecraft's EULA and any host
   terms. This repository intentionally supplies no `eula=true` or acceptance flag.
6. Start once to generate defaults. Check the console reports the pinned
   Minecraft/Paper version and both plugins without errors. Send `stop`; wait
   until save completion and the panel shows the process offline. Do not use Kill.
7. Follow `config/README.md` to capture defaults and produce the initial config
   proposal using the real allocations. Review changes and upload only the two
   config files while stopped. Keep Floodgate's entire generated directory intact.
8. Start; verify online-mode, whitelist, Floodgate authentication and listeners
   in the console. Keep outside access restricted until whitelist is confirmed.
   Add testers with panel console commands (omit the `/`):

```text
whitelist on
whitelist add JavaPlayerName
fwhitelist add ExactXboxGamertag
whitelist list
```

Use `fwhitelist` for Floodgate accounts, without the `.` prefix; consult its help
for gamertags containing spaces or use the verified Floodgate UUID. Do not guess
identities. For an operator, verify the online in-game name first, then `op NAME`;
Bedrock's displayed name normally has the `.` prefix and spaces replaced with
underscores. Account linking can change identity; verify it before granting
permissions. Test `deop NAME` and rejection of privileged commands after revocation.
Keep ordinary testers non-operators. Do not commit whitelist/ops files or gamertags.

9. Remove the temporary network restriction once whitelist enforcement is proven;
   run the first milestone tests in TEST_PLAN. Check both clients from outside the
   host network. A Java connection does not test the Bedrock listener.
10. Stop cleanly, make an off-host snapshot, restore to a separate instance, run
    both clients again, then record actual results. Only then mark milestone 1 done.

## Upgrades (deliberately separate from initialization)

1. Create a review branch. Check current upstream compatibility and security
   notes; deliberately choose exact new builds, official immutable URLs and
   published hashes. Update lock and compatibility validation/tests together.
   If an official artifact disappears, fail; never substitute `latest`.
2. Notify players, cleanly stop, disable automatic restart, make a full verified
   off-host backup, and complete a restore drill. Retain the old lock/package
   and exact Java runtime record. Do not proceed with an untested recovery path.
3. Restore into a **separate** instance with separate ports and sufficient memory.\n   Use the Windows PC per `docs/PC_STAGING.md` for the first recovery rehearsal.
   Stage the new JARs there. Keep worlds, configs, permissions and keys. Review
   migrations using a three-way comparison: old generated defaults, current
   operator configs and new generated defaults. Apply only reviewed changes.
   Never use `render-initial` to refresh production configs. Remove old duplicate
   versions of the same plugins only after identifying and backing them up.
4. Run functional/restart/recovery tests and a representative performance check.
   Check logs for removed/unknown keys and plugin failures. Record the staged
   diff and outcome. Reject the update if authentication or data changes fail.
5. Schedule a maintenance window. If production resumed after staging, stop it
   again and take a fresh snapshot. Apply the same tested software/config changes
   to the current production data; do not overwrite fresh progress with stale
   staging worlds. Verify files after transfer by downloading/comparing hashes
   if the panel cannot provide them. Start and repeat join/restart checks.
6. Rollback on regression: stop, preserve the failed state privately, restore the
   matching pre-upgrade **software + configuration + all worlds/player data +
   secrets + runtime** into a clean instance. Never downgrade just the server JAR
   against a world already written by a newer version. Document any lost progress.

For a **Geyser/Floodgate-only** update that keeps the identical Paper binary and Java\nruntime, follow `docs/PLUGIN_UPDATES.md` and verify the narrow package produced by\n`scripts/plugin_update.py` instead of blindly uploading a full release. This is\nnot a shortcut around backup, stage, join and identity tests. CoreProtect remains\nblocked by the compatibility gate in `docs/COREPROTECT.md`.\n\nAutomated deployment is a future task only after host capabilities are proven.
It must be manually triggered, use a protected production environment and secret
storage, verify backups and target identity, and refuse destructive world changes.

## Portability

Maintain a full stopped server-root copy plus runtime/port notes outside the
host. Paper stores the overworld and dimension folders separately; copy all of
them, not only `world`. Preserve UUID-based player data, plugin state, keys and
version records. At a new host, restore the same software first, change only
allocated network/bind settings, and repeat milestone 1 before redirecting players.
