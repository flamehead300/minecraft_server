# CoreProtect anti-grief logging — requested addition, compatibility gate

Decision: include CoreProtect in the operational plan and acceptance tests, but **do not install an unverified build** on Paper 26.3.

As checked 2026-10-30:
- Official public **CoreProtect Community Edition v24.1** release is explicitly marked compatible through **Minecraft 26.2**, not 26.3. Reference: https://hangar.papermc.io/CORE/CoreProtect/versions/24.1
- Publisher lists **CoreProtect v25.1** for Minecraft 26.3+ on Patreon; entitlement/download/checksum have not been verified for this project. https://www.patreon.com/cw/coreprotect/sitemap
- The official CoreProtect/Modrinth pages mention 26.3 downloads but do not supply an approved immutable 26.3-compatible artifact + verified SHA-256 in this repository. **Do not use `coreprotect.net/latest` in a lock or install a random fork.**

Acceptance for adding to `versions.lock.json` and package:
1. Obtain a lawful developer-published version compatible with Paper 26.3, immutable official URL, SHA-256 from official metadata or verified authenticated artifact, and distribution permission. Record source and check date; do not store Patreon account tokens or private artifacts in Git.
2. Extend allowlisted binary validation, manifest, download and Windows/Linux tests. If this cannot be done, install manually in **PC staging only**, with an explicitly recorded SHA-256 and no unverified production release.
3. Boot once, let the plugin generate its own `plugins/CoreProtect/` configuration and database; never invent keys. Do not commit its runtime data or include it in deployment packages.
4. Prefer default embedded database if supported by the selected version. CoreProtect 25+ docs describe DuckDB by default, which can download JDBC dependencies at runtime; verify Java/host outbound network support. Never assume a database backend when plugin versions differ.
5. Configure permissions for trusted admins only. Verify block/place/break, chest transactions and rollback/restore on **staging**. Prevent unrestricted rollback access for regular players. Test both Java and Floodgate identities separately.
6. Include **all** `plugins/CoreProtect/` database/WAL/state files in stopped backups (plus external database export if configured). Restore and query existing history. A rollback plugin is not a disaster backup.
7. Review privacy/retention: CoreProtect may log user identity, chat, commands and inventory actions. Treat DB backups and logs as player data, encrypt off-host, document policy, restrict access, consider local legal obligations.
8. Re-measure 5/10/20-user MSPT/CPU/disk writes with CoreProtect enabled before approving 20-user target.

Status: **PLANNED / BLOCKED ON COMPATIBLE PIN + VERIFIED TESTING**; do not claim the plugin is packaged or running.
