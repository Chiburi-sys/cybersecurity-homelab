# SOC Playbook — Suspicious Process Execution

**Playbook ID:** PB-002  
**Author:** Stacy Bostick  
**Last Updated:** 2026-03-01  
**Severity:** High  
**MITRE ATT&CK:** T1059 — Command and Scripting Interpreter

---

## 1. Detection

### Trigger Conditions

- Splunk alert: `Suspicious Process Execution Detected` fires
- Sysmon EventCode 1 logs PowerShell, cmd.exe, mshta.exe, certutil, or other LOLBins

### Detection Query

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  (Image="*powershell*" OR Image="*cmd.exe*" OR Image="*mshta*"
   OR Image="*certutil*" OR Image="*wscript*" OR Image="*cscript*"
   OR Image="*regsvr32*" OR Image="*rundll32*")
| table _time, User, Image, CommandLine, ParentImage, ParentCommandLine
| sort -_time
```

---

## 2. Triage (First 5 Minutes)

### Step 1: Review the Process Details

- [ ] What executable was launched?
- [ ] What was the full command line?
- [ ] What was the parent process? (Who spawned it?)
- [ ] Which user account ran it?

### Step 2: Assess Legitimacy

| Indicator | Likely Benign | Likely Malicious |
|---|---|---|
| Parent Process | explorer.exe, services.exe | winword.exe, outlook.exe, wscript.exe |
| Command Line | Simple path, no flags | Encoded commands, -nop, -w hidden, -enc |
| User | Administrator, SYSTEM | Standard user running admin tools |
| Time | Business hours | 2 AM on a Saturday |

### Step 3: Check for Encoded Commands

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  Image="*powershell*" (CommandLine="*-enc*" OR CommandLine="*-e *"
  OR CommandLine="*base64*" OR CommandLine="*hidden*" OR CommandLine="*bypass*")
| table _time, User, CommandLine
```

- [ ] If encoded PowerShell is found → **Escalate immediately**

---

## 3. Investigation (Next 15 Minutes)

### Step 4: Trace the Process Tree

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  User="<SUSPICIOUS_USER>"
| table _time, Image, CommandLine, ParentImage, ProcessId, ParentProcessId
| sort _time
```

### Step 5: Check for Network Connections from the Process

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
  Image="*powershell*"
| table _time, Image, DestinationIp, DestinationPort
```

- [ ] Is the process making outbound connections?
- [ ] If connecting to external IPs → Possible C2 callback

### Step 6: Check for File Drops

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=11
  User="<SUSPICIOUS_USER>"
| table _time, Image, TargetFilename
| sort -_time
```

---

## 4. Containment

### If Confirmed Malicious

- [ ] Isolate the affected host from the network
- [ ] Kill the malicious process
- [ ] Disable the user account if compromised
- [ ] Block any identified C2 IPs at the firewall
- [ ] Preserve forensic evidence (memory dump, disk image)

---

## 5. Remediation

- [ ] Remove any dropped malware/files
- [ ] Scan the host with updated antivirus
- [ ] Reset user credentials
- [ ] Review all systems the user accessed during the compromise window
- [ ] Patch any exploited vulnerabilities

---

## 6. Key LOLBins Reference

| Binary | Legitimate Use | Abuse Scenario |
|---|---|---|
| powershell.exe | Scripting, admin | Fileless malware, C2 |
| cmd.exe | Command execution | Batch scripts, recon |
| mshta.exe | HTML apps | Execute malicious HTA |
| certutil.exe | Certificate mgmt | Download files from internet |
| regsvr32.exe | Register DLLs | AppLocker bypass, proxy execution |
| rundll32.exe | Run DLL functions | Execute malicious DLLs |
| wscript/cscript | Run VBS/JS | Execute malicious scripts |
