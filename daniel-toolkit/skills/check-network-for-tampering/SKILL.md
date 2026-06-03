---
name: check-network-for-tampering
description: Triage the current network for tampering signs — run IP-config, ARP, traceroute, public-IP, and WiFi-encryption checks, then cross-check them (rogue DNS, ARP spoofing, route hijack, VPN/proxy, weak WiFi cipher) and print a verdict table with honest, evidence-qualified commentary. Report-only; saves nothing. Use when the user asks whether a network is safe/clean/compromised, is on public/guest WiFi, or wants a quick connection security check.
---

# Check Network for Tampering — fast triage of the current network

Runs five quick diagnostic checks, cross-checks them, then prints a verdict
table and brief commentary. **Report-only** — it does not save a file and does
not modify anything.

Detailed background, sample outputs, and the "what this can / cannot tell you"
material live in:

- `${CLAUDE_SKILL_DIR}/references/examples-000-network-diagnostics.md`
- `${CLAUDE_SKILL_DIR}/references/examples-001-wifi-encryption-check.md`

---

## Step 0 — detect the platform first

Before running anything, determine the operating system, because the command
names differ. Pick the matching column from the table in Step 1 (Windows /
Linux / macOS).

**Critical WSL caveat:** If running under WSL, use the Windows `.exe` versions
of every command (`ipconfig.exe`, `arp.exe`, `tracert.exe`, `curl.exe`,
`netsh.exe`). WSL's own namespace shows the wrong (Hyper-V) adapter — a
`172.x` virtual address, not the real Wi-Fi adapter — which is useless for
this purpose.

## Step 1 — announce, then run all five checks

`traceroute` / `tracert` is the slow one (can take 30–60s even with a hop
cap). Most shells only return when the command exits, so send a chat message
first so the user isn't staring at silence:

> 🟢 **Running network checks** — IP config, ARP, traceroute (capped 15 hops,
> 2s/probe), public IP, WiFi encryption. ~30–60s.

Then run the five diagnostic commands and capture their combined output (you
can concatenate them into one invocation). If any individual command fails,
keep going — partial output is still useful; just note which check is missing
in the report.

| # | Check | Windows | Linux | macOS |
|---|---|---|---|---|
| 1 | IP / DNS config | `ipconfig /all` | `ip addr` + `resolvectl status` | `ifconfig` + `scutil --dns` |
| 2 | ARP neighbors | `arp -a` | `ip neigh` (or `arp -a`) | `arp -a` |
| 3 | Route to host | `tracert -h 15 -w 2000 google.com` | `traceroute -m 15 -w 2 google.com` | `traceroute -m 15 -w 2 google.com` |
| 4 | Public IP | `curl -s ifconfig.me` | `curl -s ifconfig.me` | `curl -s ifconfig.me` |
| 5 | WiFi encryption | `netsh wlan show interfaces` | `nmcli dev wifi` (or `iw dev <iface> link`) | `airport -I` (`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport`) |

Under WSL, run the Windows column with `.exe` suffixes (see Step 0).

## Step 2 — parse the output

From the captured text, identify:

- **Active adapter** — the one with **both** an `IPv4 Address` *and* a
  non-empty `Default Gateway`. Ignore disconnected adapters, the Hyper-V / WSL
  virtual adapter (`vEthernet`), Bluetooth PAN, and the secondary virtual
  Wi-Fi adapters (`Wi-Fi 2`, `Wi-Fi 3`, `Wi-Fi 4`) that multi-radio chipsets
  like Qualcomm FastConnect expose.
- **Gateway IP**, **DNS server(s)**, **local IPv4** of the active adapter.
- **ARP entries** under the active adapter's interface. Exclude broadcast
  (`ff:ff:ff:ff:ff:ff`) and multicast (`01:00:5e:…`) rows — those are normal
  and always look "duplicated."
- **Traceroute hop 1 IP**, **hop 2 IP + hostname**. The hostname at hop 2 is
  the strongest cue for ISP identity.
- **Public IP** from the `curl` check.
- **SSID, Authentication, Cipher** from the connected interface block of the
  WiFi check.

## Step 3 — apply the five cross-checks

Each becomes one row in the verdict table.

| # | Check | OK when… | Flag when… |
|---|---|---|---|
| 1 | DNS server | Equals the gateway, is RFC1918, or is a known public resolver (`1.1.1.1`, `1.0.0.1`, `8.8.8.8`, `8.8.4.4`, `9.9.9.9`, `149.112.112.112`) | Anything else — especially a random public IP, or one geolocating to a country the user doesn't live in |
| 2 | ARP table | Every unicast IP has a unique MAC | Two distinct unicast IPs share a MAC (textbook ARP spoofing) |
| 3 | Traceroute hop 1 | Equals the gateway from the IP config | Hop 1 is a public IP, or doesn't match the gateway |
| 4 | Public IP vs hop 2 | Same `/16` (first two octets match) | Different `/16` — note, then ask whether a VPN / proxy is active |
| 5 | WiFi encryption | `WPA2-Personal` or `WPA3-Personal` + `CCMP` (or `GCMP`) | `WEP` / `TKIP` → flag; `Open` + `None` → **note, not flag** (normal for guest WiFi, HTTPS does the work) |

### Honest-evidence rules

- The same-`/16` heuristic in row 4 is *suggestive* of same-ISP, **not**
  WHOIS-verified. Say so explicitly in the row's "Reading" cell if the values
  match by /16 only.
- ASN / ISP attribution from hop 2's hostname (e.g. `*.sdnet.net`,
  `*.swiftelNET.brookings.net`) is an **inference** from the PTR record, not a
  wire-observed fact. If you mention an ISP name, say "hostname suggests …"
  rather than asserting it.
- A gateway shown as `setup.ui.com` is the Ubiquiti UniFi default DNS name.
  The OUI of the gateway MAC corroborates this (`e4:38:83`, `78:8a:20`,
  `24:5a:4c`, `80:2a:a8`, and other Ubiquiti OUIs). Mention this as a neutral
  identification, not a red flag.
- Trailing `* * *` hops in traceroute are normal when the destination's ASN
  drops ICMP-TTL-exceeded. As long as the trace clearly reached the target's
  ASN (Google IPs typically start in the 142.x / 172.217.x / 172.253.x /
  192.178.x / 216.239.x ranges) **before** the timeouts, the timeouts are not
  a failure.

## Step 4 — print the report

Lead with a one-line headline verdict: **"Looks clean,"** **"Looks clean with
notes,"** or **"Concerns flagged — see below."**

Then this table (real values, not placeholders):

| Check | Observed | Reading |
|---|---|---|
| DNS | `<ip(s)>` | OK / FLAG — reason |
| ARP | `<N>` unicast neighbors, `<dup count>` duplicate MAC(s) | OK / FLAG |
| Traceroute hop 1 | `<ip>` (`<hostname or "no PTR">`) | OK / FLAG — matches/doesn't match gateway |
| Public IP vs hop 2 | `<public>` vs `<hop2>` — same/different /16 | OK (heuristic) / NOTE |
| WiFi | `<SSID>` — `<Auth>` / `<Cipher>` | OK / NOTE (open) / FLAG (WEP/TKIP) |

Then one short paragraph (3–5 sentences) summarizing what the table means in
plain English. Name any FLAGs explicitly and explain what they could
indicate. If no flags, compare this network's posture to the open-WiFi
baseline in
`${CLAUDE_SKILL_DIR}/references/examples-000-network-diagnostics.md` and
`${CLAUDE_SKILL_DIR}/references/examples-001-wifi-encryption-check.md` so the
user has context.

**Do not redact** anything (public IP, ISP name, ISP-hop IP) in the chat
report — this skill writes no files, so the full values belong in the
conversation.

Close with the **standard caveats** (from
`${CLAUDE_SKILL_DIR}/references/examples-000-network-diagnostics.md`,
"What this can not tell you") — one line each:

- Whether the *router itself* is malicious / has been replaced (evil twin).
- Whether someone passively records radio frames (open WiFi → trivial).
- Whether a flaw exists higher up the stack (browser, app, OS).

## WiFi encryption decision table

Use this to interpret the `Authentication` / `Cipher` values from check 5
(from `examples-001`):

| `Authentication` | `Cipher` | What it means | What to do |
|---|---|---|---|
| `Open` | `None` | No WiFi encryption (typical guest WiFi) | Rely on HTTPS; consider VPN for general browsing. |
| `WEP` | `WEP` | Obsolete, broken since mid-2000s | Treat as unencrypted; avoid if you can. |
| `WPA2-Personal` | `CCMP` | Standard secure home/office | Good. Make sure passphrase is long/random. |
| `WPA2-Personal` | `TKIP` | Weak cipher fallback | Update router config to force CCMP/AES. |
| `WPA3-Personal` | `CCMP` (GCMP on some) | Modern, best for shared networks | Best. Devices on the same SSID can't snoop each other. |

---

## Notes for the assistant

- **Detect the platform first**, and under WSL use the Windows `.exe`
  versions — WSL's own `curl`/`ip` show WSL's namespace (a `172.x` Hyper-V
  address, not the Wi-Fi adapter), which is wrong for this purpose.
- **If the active-adapter heuristic finds zero or more than one match**, list
  the candidates and ask the user which one to analyze rather than guessing.
  (Common on machines with multiple connected interfaces, e.g. Ethernet +
  Wi-Fi both up.)
- **If the WiFi check reports multiple interfaces, only the one whose state is
  `connected` counts.** Secondary radios on Qualcomm FastConnect chipsets show
  up as `Wi-Fi 2/3/4` and will be disconnected — ignore them.
