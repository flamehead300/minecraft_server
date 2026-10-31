# Official-source verification — 2026-10-30 (America/Chicago)

## Software selection

| Source | Observed result |
| --- | --- |
| https://docs.papermc.io/paper/getting-started/ | Paper 26.1+ requires Java 25. |
| https://fill.papermc.io/v3/projects/paper/versions/26.3/builds/231 | Stable build 231; exact official URL and SHA-256 recorded in lock. |
| https://geysermc.org/wiki/geyser/supported-versions/ | Geyser supports Bedrock 26.40–26.60 and emulates Java 26.3; choose matching Paper to avoid an additional translation plugin. |
| https://download.geysermc.org/v2/projects/geyser/versions/2.12.1/builds/1279 | Spigot download hash and exact build recorded; development snapshot descriptor is intentional. |
| https://download.geysermc.org/v2/projects/floodgate/versions/2.2.5/builds/141 | Spigot download hash and exact build recorded; change metadata says update to 26.3. |
| https://geysermc.org/wiki/geyser/setup/ | Current configuration uses `java.auth-type` and `bedrock.transport`; do not copy historical `remote` examples blindly. |
| https://geysermc.org/wiki/geyser/port-forwarding/ | NetherNet needs TCP signaling and UDP gameplay; selected single NetherNet mode requires a separate port from Java TCP. Dual RakNet/NetherNet mode would require additional planning. |
| https://geysermc.org/wiki/floodgate/setup/ | Install Floodgate-Spigot and set Geyser auth type to Floodgate. |
| https://geysermc.org/wiki/geyser/secure-chat/ | Disable secure-profile enforcement for Bedrock chat, retaining Java online authentication. |
| https://geysermc.org/wiki/floodgate/features/ | `fwhitelist add GAMERTAG` without the username prefix; UUID form also supported. |
| https://geysermc.org/wiki/geyser/using-geyser-with-consoles/ | Console third-party-server workarounds exist; no general direct-entry guarantee. |

All three actual downloaded JARs matched their official SHA-256 values. ZIP
integrity checks passed. Inspected plugin descriptors: Geyser 2.12.1-SNAPSHOT,
Floodgate 2.2.5-SNAPSHOT (b141-81b65cc). Geyser's current JAR generates its config
through code rather than providing a root config.yml resource; Floodgate includes
a default config.yml. We have not represented extracted resources or synthetic
fixtures as runtime-generated defaults.

The pinned Geyser JAR's configuration class annotations also document
`webrtc-port=0` as using the Bedrock port for UDP, and `builtin` signaling as
using that port for TCP. The policy explicitly requests these settings and still
requires them to exist in the runtime-generated defaults before rendering.

Compatibility above is **documented**, not an executed crossplay result. This
workspace has Java 17, not 25. No EULA has been accepted; server boot, actual
default capture, exact host runtime and client compatibility remain unverified.
Do not silently select an older Minecraft version just to use the available JRE.

## Host evidence and remaining confirmation

| Requirement | Evidence / status |
| --- | --- |
| Premium 8 GB price | Planning estimate $18/month remains unconfirmed at checkout. Public Premium page's dynamic price was not exposed in the readable page. Recheck actual selected plan before purchase. |
| Java 25 | Host advertises all major Java versions; exact Java 25 image/vendor/patch on target instance still needs confirmation. |
| Custom JAR / plugins | Public Premium page explicitly supports custom JARs and file access. Knowledgebase version selector lists Paper, Spigot and Geyser. |
| Network | Host advertises extra ports via panel. Exact additional TCP+UDP NetherNet allocation and DDoS compatibility are pending. Historical same-port UDP instructions are insufficient for selected NetherNet mode. |
| File transfer | Host advertises FTP access; indexed file-access guide references SFTP. Confirm actual encrypted endpoint, credentials handling and host key in the panel. |
| Backups | Premium advertises daily and hourly incremental backups; indexed backup guide describes downloadable backups. Exact retention and application-consistency behavior remain pending. |
| Memory | Custom startup flags advertised; effective heap limit and total-process accounting need panel confirmation. |
| API | Knowledgebase lists an API article; no deployment API was tested or assumed. |

Official host sources consulted:

- https://pebblehost.com/minecraft/premium
- https://help.pebblehost.com/en/minecraft/choosing-a-minecraft-server-version
- https://help.pebblehost.com/en/minecraft/how-to-change-your-java-version-on-your-minecraft-server
- https://help.pebblehost.com/en/minecraft/additional-ports-system
- https://help.pebblehost.com/en/minecraft/how-to-install-geyser-and-floodgate-onto-your-minecraft-server
- https://help.pebblehost.com/en/minecraft/how-to-access-your-minecraft-servers-files
- https://help.pebblehost.com/en/minecraft/backups-explained

Several help pages rendered only an input control in the research reader;
indexed snippets and the public product page provide partial evidence. No
instance-level capability is marked tested on that basis. Direct fetching of
the Premium page from this workspace returned HTTP 403; the web reader provided
the product text but no usable 8 GB price. No purchase was attempted.

Python tooling depends on PyYAML 6.0.3. GitHub Actions pins checkout/setup-python
by commit; runner image and Python patch versions can vary. Server/plugin release
pins are distinct from toolchain dependencies. Pin the verified host Java build
in the deployment evidence; managed-host patching may require a new check.
