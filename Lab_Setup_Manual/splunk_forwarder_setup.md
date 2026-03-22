# Splunk Universal Forwarder Setup

This document explains how logs are forwarded from both the Windows 11 workstation and Windows Server 2022 (DC01) to the Splunk SIEM running on Ubuntu Server.

---

## 🧠 Overview

| Source | Destination | Port | Log Types |
|--------|-------------|------|-----------|
| Windows 11 | Ubuntu Server (Splunk) | 9997 | Sysmon, Security, Application, System |
| DC01 (Win Server 2022) | Ubuntu Server (Splunk) | 9997 | Security, System, Application, Directory Service, DNS Server |

---

## Windows 11 Workstation Forwarder

### Installation

1. Download Splunk Universal Forwarder for Windows
2. Install with administrative privileges
3. Configure inputs and outputs as shown below

### inputs.conf

```ini
[WinEventLog://Application]
disabled = 0
index = main

[WinEventLog://Security]
disabled = 0
index = main

[WinEventLog://System]
disabled = 0
index = main

[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = main
renderXml = true
```

### outputs.conf

```ini
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = 192.168.50.10:9997
```

### Verification

```spl
index=main host="WINDOWS" source="WinEventLog:Security"
| stats count by source
```

📸 **Screenshots:** `Screenshots/Win11/Win11_Splunk_*.png`

---

## Windows Server 2022 (DC01) Forwarder

### Installation

1. Downloaded Splunk Universal Forwarder MSI on DC01
2. Installed via the Setup Wizard on DC01

📸 `Screenshots/Win_Server22/DC01_Splunk_forwarder_installing.png`

### inputs.conf

Configured to collect all AD-relevant event logs:

```ini
[WinEventLog://Security]
disabled = 0
index = main

[WinEventLog://System]
disabled = 0
index = main

[WinEventLog://Application]
disabled = 0
index = main

[WinEventLog://Directory Service]
disabled = 0
index = main

[WinEventLog://DNS Server]
disabled = 0
index = main
```

📸 `Screenshots/Win_Server22/DC01_Splunk_forwarder_inputs_conf.png`

**Key log sources:**

- **Security** — Authentication events (4624, 4625, 4769), account management
- **Directory Service** — AD replication, LDAP queries
- **DNS Server** — DNS query logs for domain resolution monitoring

### outputs.conf

```ini
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = 192.168.50.10:9997

[tcpout-server://192.168.50.10:9997]
```

📸 `Screenshots/Win_Server22/DC01_Splunk_forwarder_outputs_conf.png`

### Verification

Confirm DC01 logs are arriving in Splunk:

```spl
index=main host="DC01" | stats count by source | sort -count
```

**Expected output:**

| source | count |
|--------|-------|
| WinEventLog:Security | 157 |
| WinEventLog:System | 9 |
| WinEventLog:Application | 2 |

📸 `Screenshots/Splunk/Splunk_DC01_log_sources_verified.png`

---

## 📁 Configuration File Locations

| Host | Path |
|------|------|
| Windows 11 | `C:\Program Files\SplunkUniversalForwarder\etc\system\local\` |
| DC01 | `C:\Program Files\SplunkUniversalForwarder\etc\system\local\` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No logs arriving | Verify SplunkForwarder service is running |
| Forwarder can't connect | Check firewall, ensure port 9997 is open on Ubuntu |
| Missing event types | Verify `inputs.conf` includes the right `WinEventLog://` stanzas |
| Permission errors | Run Splunk Forwarder service as Local System account |

---

*This setup guide is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
