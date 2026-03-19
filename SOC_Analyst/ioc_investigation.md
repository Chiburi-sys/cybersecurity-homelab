# IOC Investigation Workflow

**Author:** Stacy Bostick  
**Role:** Tier 1 SOC Analyst

---

## Overview

When an alert fires or a threat intel feed flags an indicator, follow this checklist to investigate and determine the scope of the threat.

---

## IP Address Investigation

### Step 1: Internal Correlation

```spl
index=main "192.168.50.30"
| stats count by source, EventCode, host
| sort -count
```

- [ ] Has this IP appeared in logs before?
- [ ] What event types are associated?
- [ ] Which hosts have been contacted?

### Step 2: Scope Assessment

```spl
index=main src_ip="192.168.50.30"
| stats dc(dest_ip) as targets, dc(dest_port) as ports, count
```

- [ ] How many internal hosts were contacted?
- [ ] How many ports were accessed?
- [ ] Is this scanning behavior or targeted?

### Step 3: Timeline Reconstruction

```spl
index=main src_ip="192.168.50.30"
| timechart span=5m count by EventCode
```

- [ ] When did activity start?
- [ ] Is it ongoing?
- [ ] Are there bursts or sustained activity?

### Step 4: OSINT Lookup (External IPs Only)

| Tool | URL | Purpose |
|------|-----|---------|
| VirusTotal | virustotal.com | Reputation, malware associations |
| AbuseIPDB | abuseipdb.com | Abuse reports, ISP info |
| Shodan | shodan.io | Open ports, services, banners |
| GreyNoise | greynoise.io | Internet-wide scanner identification |
| IPinfo | ipinfo.io | Geolocation, ASN |

- [ ] Is this IP known malicious?
- [ ] Is it a known scanner or bot?
- [ ] What country/ASN does it belong to?

---

## Domain / URL Investigation

### Step 1: Check DNS Logs

```spl
index=main sourcetype=DNS query="suspicious-domain.com"
| stats count by src_ip, query
```

### Step 2: OSINT

| Tool | Purpose |
|------|---------|
| VirusTotal | Domain reputation |
| urlscan.io | Live page scan |
| Whois | Registration details |
| DNSdumpster | DNS history |

- [ ] Is the domain newly registered (< 30 days)?
- [ ] Does it have a DGA-like pattern?
- [ ] Is it on any known threat intel lists?

---

## File Hash Investigation

### Step 1: Check for File on Endpoints

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
| search Hashes="*<HASH>*"
| table _time, host, User, Image, CommandLine
```

### Step 2: OSINT

| Tool | Purpose |
|------|---------|
| VirusTotal | Hash reputation, AV detections |
| Hybrid Analysis | Sandbox analysis |
| MalwareBazaar | Malware family identification |

- [ ] Is the hash flagged by any AV engines?
- [ ] What malware family does it belong to?
- [ ] Has it been seen on other hosts?

---

## Account Investigation

### Step 1: Recent Activity

```spl
index=main Account_Name="j.smith"
| stats count by EventCode, Source_Network_Address, host
| sort -count
```

### Step 2: Authentication Pattern

```spl
index=main Account_Name="j.smith" (EventCode=4624 OR EventCode=4625)
| table _time, EventCode, Logon_Type, Source_Network_Address, Workstation_Name
| sort _time
```

- [ ] Any logins from unusual IPs or times?
- [ ] Any failed logins followed by success?
- [ ] Any logon types unusual for this account (Type 3, Type 10)?

### Step 3: Privilege Usage

```spl
index=main Account_Name="j.smith" EventCode=4672
| table _time, Privileges
```

- [ ] Was special privilege assigned?
- [ ] Is this expected for this user's role?

---

## Investigation Decision Tree

```
Alert Received
    │
    ├── Is source IP internal?
    │       ├── YES → Check host identity, is it a known asset?
    │       │           ├── Known asset → Check user activity
    │       │           └── Unknown → Escalate (rogue device)
    │       └── NO → Run OSINT lookup
    │               ├── Known malicious → Block + Escalate
    │               └── Clean → Continue monitoring
    │
    ├── Has authentication succeeded?
    │       ├── YES → Credential compromise → Escalate
    │       └── NO → Monitor, check for spray pattern
    │
    └── Is activity ongoing?
            ├── YES → Contain first, investigate second
            └── NO → Investigate, document, close/escalate
```

---

*This IOC investigation workflow is part of a cybersecurity home lab portfolio demonstrating Tier 1 SOC Analyst skills.*
