---
id: 001
title: Checking WiFi Encryption (WPA2 / WPA3 / Open)
summary: How to tell whether the WiFi you're on uses WPA2, WPA3, or no encryption at all — and what cipher is in use.
commands: [netsh]
platform: Windows
tags: [wifi, wpa2, wpa3, encryption, ssid]
related: [examples-000-network-diagnostics.md, DEFINITIONS.md]
---

# Examples 001 — WiFi Encryption Check

A single command tells you whether the network you're on actually encrypts WiFi
frames. Spoiler: at most coffee shops and guest networks, it doesn't.

---

## 1. `netsh wlan show interfaces` — current WiFi state

**Why:** The `Authentication` and `Cipher` lines tell you exactly what's
protecting (or not protecting) traffic at the WiFi layer. If both say
`Open` / `None`, every frame in the air is unencrypted at L2 — anything you do
*above* it (HTTPS, VPN) is doing all the work.

```cmd
netsh wlan show interfaces
```

Sample output from `Cottonwood Guest`:

```text
There is 1 interface on the system:

    Name                   : Wi-Fi
    Description            : Intel(R) Wi-Fi 6 AX201 160MHz
    GUID                   : 12345678-1234-1234-1234-1234567890ab
    Physical address       : aa:bb:cc:11:22:33
    State                  : connected
    SSID                   : Cottonwood Guest                # <-- network name
    BSSID                  : 11:22:33:44:55:66
    Network type           : Infrastructure
    Radio type             : 802.11ax
    Authentication         : Open                            # <-- NOTE: no auth
    Cipher                 : None                            # <-- NOTE: no encryption
    Connection mode        : Auto Connect
    Channel                : 36
    Receive rate (Mbps)    : 1200
    Transmit rate (Mbps)   : 1200
    Signal                 : 85%
    Profile                : Cottonwood Guest
```

**Reading it:**
- `Authentication: Open` — no password, no key exchange. Anyone in radio range
  can join.
- `Cipher: None` — frames are sent in the clear at the WiFi layer.
- This is **normal for a guest network**. It's not "compromised" — it's by
  design. The trade-off is that you rely entirely on HTTPS (and optionally a
  VPN) for confidentiality.

---

## 2. What you want to see on a secured network

For comparison, on a home / office network you'd expect something like:

```text
    SSID                   : MyHomeNetwork
    Authentication         : WPA3-Personal                   # <-- or WPA2-Personal
    Cipher                 : CCMP                            # <-- AES, good
```

**Reading it:**
- `WPA2-Personal` or `WPA3-Personal` → encrypted, with WPA3 preferred (forward
  secrecy + protects users from each other).
- `CCMP` → AES-based, the strong cipher. `TKIP` would be the old/weak one.

---

## Decision table

| `Authentication` | `Cipher` | What it means | What to do |
|---|---|---|---|
| `Open` | `None` | No WiFi encryption (typical guest WiFi) | Rely on HTTPS; consider VPN for general browsing. |
| `WEP` | `WEP` | Obsolete, broken since mid-2000s | Treat as unencrypted; avoid if you can. |
| `WPA2-Personal` | `CCMP` | Standard secure home/office | Good. Make sure passphrase is long/random. |
| `WPA2-Personal` | `TKIP` | Weak cipher fallback | Update router config to force CCMP/AES. |
| `WPA3-Personal` | `CCMP` (GCMP on some) | Modern, best for shared networks | Best. Devices on the same SSID can't snoop each other. |

---

## Bonus: see *all* nearby networks and their auth

```cmd
netsh wlan show networks mode=bssid
```

This dumps every SSID in range with their `Authentication` / `Encryption`
fields — handy for spotting evil twins (two SSIDs with the same name but
different security settings or BSSIDs) or just for surveying what a venue is
running.

---

## Takeaway

`Open` / `None` at a coffee shop is expected and not by itself dangerous —
modern HTTPS handles the confidentiality piece. The real residual risks on
open WiFi are:

1. **Evil twin APs** mimicking the real SSID.
2. **Clicking through certificate warnings** when a MITM is present.
3. **Apps that don't enforce HTTPS** (rare now, but worth checking).

See [`examples-002-wireshark-first-capture.md`](./examples-002-wireshark-first-capture.md)
to actually watch what crosses an open WiFi link.
