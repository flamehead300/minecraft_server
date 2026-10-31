# Acceptance plan

Never infer production readiness from CI, idle bots, successful downloads or
an empty-server startup. Keep the whitelist enabled while testing.

## Gate 0 — repository automation

- Parse lock/policy/workflow; validate exact official HTTPS URLs, hashes, builds,
  destinations and authentication invariants.
- Run safety tests for failed HTTP/checksum/JAR checks, repeated setup, unknown
  config keys, duplicates/aliases, invalid ports, preserving unrelated settings,
  extra deployment data, backup corruption, restore collisions and symlinks.
- Download all three real official artifacts and compare published hashes.
- Build and verify exact deployment manifest; reject unexpected files.
- Check tracked files for common secrets/data. This is a heuristic, not a complete
  secret scanner. Review staged diffs manually before committing.
- GitHub runs offline tests on Linux/Windows and network artifact checks on Linux.
  Local Linux results do not imply GitHub or Windows jobs have run.

## Gate 1 — first requested milestone

Record build/lock hash, full Java runtime, host location/allocations, device/client
versions, start/end times and evidence links privately; commit redacted results.

| Test | Pass condition |
| --- | --- |
| Boot and defaults | Pinned Paper and both plugins load without exceptions; initial configuration derived from generated defaults; actual listeners match allocations. |
| Concurrent join | One licensed/authenticated Java 26.3 player and one supported signed-in Bedrock player play together from external networks. |
| Admission | Whitelisted accounts join; an unlisted account is denied for each client type. Retain `online-mode=true`; reject invalid Java login. |
| Permissions | Non-ops cannot run admin commands; verified op identity can, then cannot after deop. Include Floodgate prefix/UUID handling. |
| Movement/combat | Walk, sprint, swim, jump, interact, attack mobs and take damage without sustained desync. |
| Items | Pick up/drop/trade items between clients, craft, use containers and ender chests; quantities match with no duplication/loss. |
| Chat/sleep | Both clients send/receive chat; beds set spawn and ordinary sleep behavior works. |
| Dimensions | Both clients travel to Nether and End and return; inventories and locations remain correct. |
| Restart persistence | Record private inventory/XP/build/coordinates, clean stop/start, rejoin both identities and verify the exact state. |
| Backup recovery | Clean stop, complete off-host backup, verify hashes, restore into separate instance; both clients recover recorded state and survive another restart. |

Capture failures, reproduction steps and logs; redact IPs, names, UUIDs, tokens
and secrets before committing. A Bedrock version outside the documented range
requires an intentional compatibility review, not an unpinned hotfix.

## Gate 2 — progressively establish 20-player capacity

Run distinct 5-, 10- and 20-active-player stages, each with warmup followed by
**30 minutes of measured representative play**. Suggested mix: approximately
half Java and half Bedrock, including real clients at each stage. Document exact
counts, devices, connection regions and alternatives if representative workloads
are used. Idle bots alone are insufficient; real Bedrock networking and gameplay
must be covered even if scripted workloads supplement player counts.

Use the same recorded workload per stage, scaled with count:

- 10 minutes: survival base activity, combat, inventories, crafting, chat and sleep.
- 10 minutes: normal farms, redstone/hoppers, villagers and entities in loaded
  chunks; record actual entity counts, farm designs and concurrent dimensions.
- 10 minutes: several groups explore previously ungenerated chunks and travel
  between dimensions; record movement method, approximate distance and terrain.

Use Paper's included profiler/metrics facilities where available (verify console
help and the bundled spark version), plus panel total memory/CPU/network charts.
Use a tick-duration distribution or collected tick samples to calculate p95;
average MSPT is not p95. Save raw reports privately and commit redacted aggregates.
Report whole-run and phase-specific results. If tooling cannot provide p95, mark
that metric blocked rather than substituting the mean.

| Metric | Acceptance target |
| --- | --- |
| Tick rate | Approximately 20 TPS throughout representative operation; investigate sustained drops. |
| Tick duration | p95 < 50 ms for each documented 30-minute stage; additionally inspect exploration/farm spikes and maximum tick time. |
| Memory | Record peak and trend for heap and total/container usage; no OOM/restarts or continuing unbounded growth; measurable headroom below host cap. |
| Latency | Record per-client/mixed-client median and p95 where available, regions and disconnect counts; agree on acceptable latency for chosen location. |
| Correctness | No lost/duplicated progress, unexplained disconnects or persistent client desynchronization. |

If a stage fails, stop escalation, profile and change one variable. Log old/new
values and gameplay impact; rerun the failed stage. If generation dominates,
agree a bounded pre-generation area, pin its tool separately, schedule offline
work and measure before/after using the same route. Do not claim pre-generation
proves unbounded exploration capacity. Adjust budget/host only with authorization.

## CoreProtect extension gate (after compatible release is pinned)

Current status: NOT RUN. Only after COREPROTECT.md's immutable version/hash\nrequirement is satisfied, test CoreProtect block and container history with\nJava and Floodgate identities on PC staging. Confirm normal players cannot\ninspect or rollback histories, trusted admins can preview and reverse a small\nsynthetic grief event, and restored databases preserve logs. Repeat representative\nMSPT, disk utilization and backup timings with logging enabled. Preserve no player\nidentifiers or chat contents in GitHub results. A plugin rollback is not a full backup.\n\n## Gate 3 — safe update rehearsal

Starting from a restored snapshot with real test progress and deliberately
customized harmless config values, stage the candidate release. Verify custom
settings, keys, whitelist/ops, worlds and identities survive. Run gate 1 again.
Restore the full old snapshot into another empty instance and verify rollback.
Do not merely replace the JAR. Record versions, config diff, backup checksum,
runtime, results and any progress lost on rollback. Only then schedule production.

## Result format

Copy `docs/results/TEMPLATE.md` per milestone. Use PASS, FAIL, NOT RUN or BLOCKED;
include tester, dates, exact builds, workload, metrics and evidence. Update
HANDOFF after every milestone. Keep sensitive raw evidence outside Git.
