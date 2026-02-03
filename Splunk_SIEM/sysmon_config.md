
---

## 📄 `sysmon_config.md`

```markdown
# Sysmon Configuration (Windows 11)

This document outlines how Sysmon is installed and configured on the Windows 11 workstation to generate detailed endpoint telemetry for Splunk ingestion.

---

## 🧠 Overview

- **Tool:** Sysmon (System Monitor)  
- **Source:** Windows 11  
- **Destination:** Splunk SIEM via Universal Forwarder  
- **Purpose:** Capture process creation, network connections, file access, registry changes

---

## 🛠️ Installation Steps

1. Download Sysmon from Microsoft Sysinternals  
2. Install via command line:
```powershell
Sysmon64.exe -accepteula -i sysmon_config.xml
