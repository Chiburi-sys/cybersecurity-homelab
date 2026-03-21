# Portfolio Showcase: SIEM Engineering & Threat Detection

**Analyst:** Stacy Bostick
**Core Competencies:** Splunk Enterprise, Sysmon, SPL Detection Engineering, Threat Hunting

---

## 🛡️ Project Overview: Enterprise SIEM Deployment

Architected and deployed a comprehensive SIEM environment using **Splunk Enterprise** on an Ubuntu Server. Integrated **Sysmon** and Splunk Universal Forwarders across a multi-VM lab to collect, normalize, and analyze high-fidelity endpoint telemetry and Windows Security Logs.

The goal of this deployment was to establish deep visibility into process execution, network connections, and authentication behavior to detect advanced persistent threats (APTs) and create custom, actionable alerts.

---

## 🔍 Detection Engineering & SPL Expertise

Below is a curated selection of custom Splunk Processing Language (SPL) queries developed to detect specific MITRE ATT&CK techniques within the environment.

### 🔴 Credential Access: Brute Force Detection

*Identifies repeated failed login attempts indicative of a brute force or password spraying attack.*

**Failed Logins Grouped by Source IP (Threshold > 5)**

```spl
index=main EventCode=4625
| stats count by src_ip
| where count > 5
| sort -count
```

### 🟢 Network Reconnaissance: Port Scan Detection

*Leverages Sysmon Event ID 3 (Network Connection) to detect abnormal outbound scanning behavior from a single endpoint.*

**Port Scan Detection (20+ Unique Ports Target)**

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| stats dc(DestinationPort) as unique_ports by SourceIp
| where unique_ports > 20
| sort -unique_ports
```

### 🛡️ Defense Evasion: Suspicious Process Execution

*Monitors for Living off the Land (LotL) binaries often abused by threat actors for execution and evasion.*

**Suspicious PowerShell/CMD/Certutil Execution**

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  (Image="*powershell*" OR Image="*cmd.exe*" OR Image="*certutil*" OR Image="*mshta*")
| stats count by Image, CommandLine, User
| sort -count
```

---

## 📊 Dashboard Development capabilities

Proficient in translating complex datasets into actionable visualizations for Tier 1 and Tier 2 SOC Analyst monitoring.

* **Security Event Distribution:** Utilizing `| top EventCode` on `LogName=Security` to visualize the overall health and volume of Windows authentication and permission changes.
* **Firewall Telemetry:** Tracking allowed vs. blocked connections via Event Codes 5156 and 5157, mapped against known malicious infrastructure.

---
*Available for freelance SIEM configuration, SPL query development, and Threat Hunting consultations.*
