# Splunk Universal Forwarder Setup (Windows 11 → Splunk SIEM)

This document explains how logs are forwarded from the Windows 11 workstation to the Splunk SIEM running on Ubuntu Server using Splunk's Universal Forwarder.

---

## 🧠 Overview

- **Source:** Windows 11 workstation  
- **Destination:** Ubuntu Server (Splunk Enterprise)  
- **Forwarder:** Splunk Universal Forwarder  
- **Telemetry:** Sysmon logs, Windows Event Logs

---

## 🛠️ Installation Steps

1. Download Splunk Universal Forwarder for Windows  
2. Install with administrative privileges  
3. Configure inputs to monitor:
   - Sysmon logs (`Application`, `System`, `Microsoft-Windows-Sysmon/Operational`)
   - Security logs
4. Set up outputs to forward to Splunk Enterprise:
   - IP: `192.168.50.10`
   - Port: `9997` (default Splunk TCP input)

---

## 📁 Configuration Files

- `inputs.conf` — Defines which logs to monitor  
- `outputs.conf` — Specifies Splunk destination  
- `props.conf` — Optional field extraction and formatting

---

## 🔍 Verification

- Confirm logs are arriving in Splunk via `index=main` or `index=sysmon`  
- Use SPL queries to validate ingestion:
```spl
index=sysmon EventCode=1
| stats count by Image
