# PebbleHost pre-purchase checklist — 2026-10-30

**Status: purchase blocked pending direct host confirmation.** Public help pages describe product features, not capabilities of a particular 8 GB Premium allocation. This document records published evidence, questions to send, and operator-only replies; no ticket has been sent.

| Check | Published evidence | Decision |
| --- | --- | --- |
| 8 GB Premium | Official billing catalog lists $18/month | Listed price confirmed; taxes, location, add-ons, availability and final checkout remain open |
| Java 25 | Host advertises major Java releases | Exact Java 25 vendor/full build and selectable image UNCONFIRMED |
| Paper/plugins | Custom server JAR and plugin uploads documented | Product-level support documented; verify our exact JAR and disable auto-reinstall |
| Bedrock port | Additional ports advertised | Separate public port on BOTH TCP and UDP, NetherNet signaling/gameplay and DDoS treatment UNCONFIRMED |
| SFTP | Official File Manager → SFTP Details instructions | Documented; actual endpoint/fingerprint and permissions pending |
| Premium backups | 4 manual slots, 7-day manual retention; export links; access to automatic backups may depend on optional plan | Published; exact effective retention, storage, download permission and restore granularity pending |
| Scheduler | Advanced → Scheduled Tasks supports Power Action and Send Command, offsets, Continue on failure | No documented native **Create Backup** action in that list; stop → backup → start must NOT be enabled unless host confirms a supported backup task/API and completion barrier |

References:
- https://billing.pebblehost.com/index.php?rp=%2Fstore%2Fpremium-minecraft-hosting
- https://help.pebblehost.com/en/minecraft/how-to-set-up-scheduled-tasks
- https://help.pebblehost.com/en/minecraft/backups-explained
- https://help.pebblehost.com/en/minecraft/how-to-access-your-minecraft-servers-files
- https://help.pebblehost.com/en/minecraft/how-to-change-your-servers-versionjar-file
- https://geysermc.org/wiki/geyser/port-forwarding/

## Pre-sales message (send via https://billing.pebblehost.com/submitticket.php or support Discord)

Subject: Pre-purchase questions: Premium 8 GB, Paper 26.3 + Geyser NetherNet

I'm considering an 8 GB Premium Minecraft server for about 20 combined Java/Bedrock players, using Paper 26.3 on Java 25 with Geyser-Spigot and Floodgate-Spigot. Before purchase, please confirm:

1. Can this exact product/location select Java 25? Which runtime vendor, current full version/build, and update policy? Can I set a 6 GiB max Java heap while leaving process headroom?
2. Can I use a custom Paper server.jar and upload plugins/configurations without the panel overwriting them on restart or auto-updating the JAR?
3. Can I allocate a SECOND public port distinct from Java that is reachable on **both TCP and UDP with the same port number** for Geyser NetherNet? Do filtering, reverse proxies or advanced DDoS modes affect TCP signaling or UDP/WebRTC? Is it included in the 8 GB price?
4. Is SFTP enabled with upload/download of the entire server tree, including plugin databases and private plugin files? Can I verify the SSH host-key fingerprint?
5. What manual and automatic backup frequencies, slot limits, retention, charges, download formats, and off-instance export options apply to this 8 GB plan? Can a full backup be downloaded without restoring it?
6. Does Advanced → Scheduled Tasks support a **native backup task**, in addition to power and console commands? If yes, can it enforce an actual completion dependency: clean stop → backup finishes successfully → start, and prevent overlapping schedules? What happens on failure or timeout? If no, what supported alternative is available?
7. Can I provision a second isolated testing instance temporarily for a real restore rehearsal, and how is it billed? What would the final monthly total be for 8 GB in the proposed location including required ports and backups?

Please answer each question specifically for the Premium 8 GB plan; documentation links are appreciated.

## Evidence log

- 2026-10-30: Public docs checked, support response **NOT RECEIVED**.
- Ticket/Discord link and response ID: PENDING.
- Exact Java runtime and Java/Bedrock ports: PENDING.
- Scheduler backup action, completion semantics, failure handling: PENDING.
- Final price/terms: PENDING.
- Go/no-go: **NO-GO** until (1), (3), (4), backup access and practical stop/backup/start procedure are resolved. Do not rely on a fixed delay as proof that shutdown or backup completed.
