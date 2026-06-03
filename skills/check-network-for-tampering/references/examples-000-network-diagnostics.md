---
id: 000
title: Network Diagnostics from the Command Line
summary: Built-in Windows commands to inspect IP config, ARP table, and the path to a remote host. Used to triage "is this network compromised?"
commands: [ipconfig, arp, tracert, curl]
platform: Windows
tags: [diagnostics, dns, arp, routing, public-ip]
related: [examples-001-wifi-encryption-check.md]
---

# Examples 000 — Network Diagnostics

Quick checks that surface red flags (rogue DNS, ARP spoofing, weird routes)
without installing anything. None of these *prove* a network is clean — a
sophisticated attack hides at a layer these commands can't see — but they're
cheap and they catch the dumb stuff.

Captured live from `Cottonwood Guest` (an open guest WiFi). Public IP, ISP
name, and ISP-hop IP are redacted.

---

## 1. `ipconfig /all` — full interface and DNS configuration

**Why:** Confirms which DNS servers your machine is using. A surprise DNS
server (not your router, not a known public resolver like `1.1.1.1` or
`8.8.8.8`) is a classic sign of tampering.

```cmd
ipconfig /all
```

Sample output (trimmed to the active WiFi adapter):

```text
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Intel(R) Wi-Fi 6 AX201 160MHz
   Physical Address. . . . . . . . . : AA-BB-CC-11-22-33
   DHCP Enabled. . . . . . . . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 192.168.1.142(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
   DNS Servers . . . . . . . . . . . : 192.168.1.1            # <-- NOTE
```

**Reading it:**
- `Default Gateway` is your router on the local subnet — normal.
- `DNS Servers = 192.168.1.1` means the router is resolving DNS. Also normal.
  If this said `45.x.x.x` or pointed to a country you don't live in, that's a
  red flag.

---

## 2. `arp -a` — neighbors on the local network

**Why:** ARP maps IPs to MAC addresses on the local subnet. **Two IPs sharing
the same MAC** is the textbook signature of ARP spoofing — an attacker
pretending to be the gateway to intercept your traffic.

```cmd
arp -a
```

Sample output:

```text
Interface: 192.168.1.142 --- 0x10
  Internet Address      Physical Address      Type
  192.168.1.1           00-11-22-aa-bb-cc     dynamic     # <-- gateway
  192.168.1.50          00-11-22-dd-ee-ff     dynamic
  192.168.1.87          00-11-22-99-88-77     dynamic
  192.168.1.255         ff-ff-ff-ff-ff-ff     static      # broadcast
  224.0.0.22            01-00-5e-00-00-16     static      # multicast
```

**Reading it:**
- Each `Internet Address` has a unique `Physical Address`. Good.
- If `192.168.1.1` and `192.168.1.50` had the **same MAC**, that's an attacker
  impersonating the gateway. None of that here.
- `ff-ff-ff-ff-ff-ff` (broadcast) and the `01-00-5e-…` multicast MACs are
  normal — ignore them.

---

## 3. `tracert google.com` — path to a known destination

**Why:** The first hop should be your own gateway. The rest of the path should
look geographically plausible (your city → a regional ISP hub → the target).
Sudden detours through unexpected countries or a missing first hop both
warrant a closer look.

```cmd
tracert google.com
```

Sample output (ISP hop redacted):

```text
Tracing route to google.com [142.250.190.46]
over a maximum of 30 hops:

  1     1 ms     1 ms     1 ms  192.168.1.1                       # <-- gateway
  2     8 ms     9 ms     8 ms  <ISP_HOP_IP>                      # <-- redacted ISP edge
  3    14 ms    12 ms    13 ms  ae-12.r01.<city>.<isp>.net
  4    22 ms    21 ms    22 ms  ae-3.r02.denver.example.net
  5    23 ms    23 ms    24 ms  108.170.245.65
  6    24 ms    24 ms    24 ms  142.250.190.46

Trace complete.
```

**Reading it:**
- Hop 1 = `192.168.1.1` — matches the gateway from `ipconfig`. Good.
- Hop 2 = ISP edge router. Stable, low latency, in the right region.
- Latencies climb gradually. No `* * *` blackholes early in the path.
- If hop 1 were a public IP, or hop 2 lived in a country you don't, that's a
  red flag.

---

## 4. `curl ifconfig.me` — your public IP

**Why:** Tells you the IP the internet sees you as. Useful to confirm a VPN is
on (or off), and to compare against the ISP hop in `tracert`.

```cmd
curl ifconfig.me
```

Sample output:

```text
<PUBLIC_IP>
```

**Reading it:**
- Compare against the second hop in `tracert`. They should belong to the same
  ISP / ASN. If `curl` shows a random datacenter IP and you're not on a VPN,
  something is routing your traffic somewhere you didn't expect.
- Alternative if you don't have `curl`: open a browser to
  [https://ifconfig.me](https://ifconfig.me) or Google "what is my IP".

---

## What "clean" looks like — summary from this session

| Check | Expected | Observed on `Cottonwood Guest` |
|---|---|---|
| DNS server | Router or known resolver | `192.168.1.1` (router) — OK |
| ARP table | No duplicate MACs | No duplicates — OK |
| Tracert hop 1 | Local gateway | `192.168.1.1` — OK |
| Public IP | Matches ISP in tracert hop 2 | Matches — OK |

No red flags. The network is **open** (no WiFi encryption — see
[examples-001](./examples-001-wifi-encryption-check.md)) but not visibly
*compromised*. HTTPS still protects content.

---

## What this can **not** tell you

- Whether the *router itself* is malicious / has been replaced (evil twin).
- Whether someone passively records radio frames (open WiFi → trivial).
- Whether a flaw exists higher up the stack (browser, app, OS).

For those, you need the browser padlock + cert check, monitor-mode capture,
and endpoint security respectively.
