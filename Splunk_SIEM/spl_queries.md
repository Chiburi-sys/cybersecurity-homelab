# Splunk SPL Query Reference — SOC Analyst Toolkit
**Analyst:** Stacy  
**Environment:** Splunk Enterprise 10.2.0 on Ubuntu Server  
**Data Sources:** Windows Security Logs, Sysmon (via Universal Forwarder)
---
## Quick Reference
This document contains all SPL (Search Processing Language) queries used for threat detection, incident investigation, and dashboard building in the home lab SIEM environment.
---
## 🔴 Brute Force Detection
### Failed Login Attempts
```spl
index=main EventCode=4625
| table _time, Account_Name, Source_Network_Address, Failure_Reason
| sort -_time
```
### Failed Logins Grouped by Source IP
```spl
index=main EventCode=4625
| stats count by src_ip
| where count > 5
| sort -count
```
### Failed Login Timeline (Dashboard Panel)
```spl
index=main EventCode=4625
| timechart span=1m count
```
---
## 🟢 Authentication Monitoring
### Successful Logins by Account
```spl
index=main EventCode=4624
| stats count by Account_Name
| sort -count
```
### Logins from Specific IP
```spl
index=main EventCode=4624 Source_Network_Address="192.168.50.30"
| table _time, Account_Name, LogonType, Source_Network_Address
```
### Logon Type Reference
| LogonType | Description                |
|-----------|----------------------------|
| 2         | Interactive (console)      |
| 3         | Network (SMB, mapped drive)|
| 7         | Unlock                     |
| 10        | RemoteInteractive (RDP)    |
---
## 🔍 Network Reconnaissance Detection
### All Events from a Specific IP
```spl
index=main "192.168.50.30"
| stats count by source, EventCode
| sort -count
```
### Port Scan Detection (20+ Unique Ports)
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| stats dc(DestinationPort) as unique_ports by SourceIp
| where unique_ports > 20
| sort -unique_ports
```
### Network Connections by Source IP & Port
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| stats count by SourceIp, DestinationPort
| sort -count
| head 20
```
---
## 🛡️ Process Monitoring (Sysmon)
### Top Processes Created
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
| stats count by Image
| sort -count
| head 20
```
### Suspicious Process Execution
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  (Image="*powershell*" OR Image="*cmd.exe*" OR Image="*certutil*" OR Image="*mshta*")
| stats count by Image, CommandLine, User
| sort -count
```
### Process Creation with Full Command Line
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
| table _time, User, Image, CommandLine, ParentImage
| sort -_time
```
---
## 📊 Dashboard Queries
### Security Event Distribution (Pie Chart)
```spl
index=main LogName=Security
| top EventCode
```
### All Windows Events by Source
```spl
index=main
| stats count by source
| sort -count
```
### Event Volume Over Time
```spl
index=main
| timechart span=1h count by source
```
---
## 🔥 Windows Firewall Logs
### Allowed Connections
```spl
index=main EventCode=5156
| table _time, Application, SourceAddress, DestinationAddress, DestinationPort
| sort -_time
```
### Blocked Connections
```spl
index=main EventCode=5157
| table _time, Application, SourceAddress, DestinationAddress, DestinationPort
| sort -_time
```
### Firewall Events from Attacker IP
```spl
index=main (EventCode=5156 OR EventCode=5157) "192.168.50.30"
| table _time, EventCode, DestinationAddress, DestinationPort
```
---
## 🧩 Sysmon Event Code Reference
| EventCode | Description                     | Use Case                          |
|-----------|----------------------------------|-----------------------------------|
| 1         | Process Creation                 | Detect malware execution          |
| 2         | File Creation Time Changed       | Detect timestomping               |
| 3         | Network Connection               | Detect C2 callbacks, port scans   |
| 5         | Process Terminated               | Track process lifecycle           |
| 7         | Image Loaded                     | Detect DLL injection              |
| 8         | CreateRemoteThread               | Detect process injection          |
| 10        | Process Access                   | Detect credential dumping         |
| 11        | File Created                     | Detect dropped files              |
| 12/13/14  | Registry Events                  | Detect persistence mechanisms     |
| 22        | DNS Query                        | Detect DNS-based C2               |
---
## 📌 Windows Security Event Code Reference
| EventCode | Description                     | Use Case                          |
|-----------|----------------------------------|-----------------------------------|
| 4624      | Successful Login                 | Monitor legitimate access         |
| 4625      | Failed Login                     | Detect brute force attacks        |
| 4634      | Account Logoff                   | Session tracking                  |
| 4648      | Explicit Credential Logon        | Detect pass-the-hash              |
| 4672      | Special Privileges Assigned      | Monitor admin activity            |
| 4688      | Process Creation                 | Track new processes               |
| 4698      | Scheduled Task Created           | Detect persistence                |
| 4720      | User Account Created             | Detect unauthorized accounts      |
| 5156      | Firewall: Connection Allowed     | Network monitoring                |
| 5157      | Firewall: Connection Blocked     | Detect blocked attacks            |
---
*This query reference is maintained as part of a cybersecurity home lab portfolio for SOC analyst skill development.*
