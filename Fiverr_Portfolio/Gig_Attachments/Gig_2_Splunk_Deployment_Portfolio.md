# Portfolio Showcase: Splunk SIEM Deployment & Dashboard Development

**Stacy Bostick** | Google Certified Cybersecurity Professional

---

## Project Overview: Enterprise SIEM Deployment

Designed and deployed a full Splunk Enterprise SIEM environment from scratch, including server installation, Universal Forwarder configuration across multiple endpoints, and custom SOC dashboard development.

---

## Deployment Architecture

**Environment:**

- Splunk Enterprise Server on Ubuntu Server 22.04
- Splunk Universal Forwarders on Windows Server 2022 (Domain Controller) and Windows 11 Workstations
- Log sources: Windows Event Logs, Sysmon, Active Directory audit logs

**Key Configurations:**

- Configured `inputs.conf` and `outputs.conf` on each forwarder for targeted log collection
- Set up receiving ports and index management on the Splunk server
- Deployed Sysmon with a custom XML configuration for enhanced endpoint telemetry

---

## Dashboard Development

Built a custom "SOC Overview" dashboard providing a single pane of glass for security monitoring:

- **Failed Login Tracker:** Real-time timechart of Event ID 4625 (failed logons) across all endpoints
- **Attack Source Map:** Table of top source IPs generating security events
- **Event Volume Panel:** Monitoring daily log ingestion rates to ensure data flow health

---

## Sample SPL Queries Used

**Brute Force Detection:**

```
index=main EventCode=4625 | stats count by src_ip, dest | where count > 5
```

**Suspicious Process Monitoring:**

```
index=main source="WinEventLog:Sysmon" EventCode=1
| search (process_name="powershell.exe" OR process_name="cmd.exe")
| table _time, host, user, process_name, CommandLine
```

---

## Tools & Technologies

Splunk Enterprise | Splunk Universal Forwarder | Sysmon | Windows Event Logs | Ubuntu Server | Active Directory | SPL (Search Processing Language)

---

*This document showcases deployment methodology and final deliverables. Specific configurations are tailored to each client's unique environment.*
