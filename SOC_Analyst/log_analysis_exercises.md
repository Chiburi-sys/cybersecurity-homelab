# Splunk Log Analysis Exercises

**Purpose:** Practice the SPL queries asked in SOC analyst interviews  
**Environment:** cybersec.local — Splunk Enterprise on 192.168.50.10  
**Index:** main

---

## Exercise 1: Find All Failed Logins in the Last Hour

**Scenario:** The SOC manager asks you to quickly check for failed logins.

```spl
index=main EventCode=4625 earliest=-1h
| table _time, Account_Name, Source_Network_Address, Failure_Reason
| sort -_time
```

**What to look for:** Burst patterns from a single IP, multiple accounts targeted, unusual times.

---

## Exercise 2: Top 10 Source IPs by Failed Login Count

**Scenario:** Identify which IPs are generating the most authentication failures.

```spl
index=main EventCode=4625
| stats count by Source_Network_Address
| sort -count
| head 10
```

**Follow-up:** For the top IP, check if any logins succeeded:

```spl
index=main EventCode=4624 Source_Network_Address="<TOP_IP>"
| table _time, Account_Name, Logon_Type
```

---

## Exercise 3: Which Account Had the Most Failed Logins Today?

**Scenario:** Determine if a specific account is under attack.

```spl
index=main EventCode=4625 earliest=-24h
| stats count by Account_Name
| sort -count
| head 5
```

**What this tells you:** If one account has 100+ failures and others have 2-3, it's a brute force. If many accounts have similar failure counts, it's a password spray.

---

## Exercise 4: Show All Processes Spawned by cmd.exe

**Scenario:** Hunt for post-exploitation command execution.

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  ParentImage="*cmd.exe*"
| table _time, host, User, Image, CommandLine, ParentCommandLine
| sort -_time
```

**Red flags:** `whoami`, `net user`, `net group`, `ipconfig`, `systeminfo` — standard recon commands.

---

## Exercise 5: What IPs Connected to the DC on Port 445 (SMB)?

**Scenario:** Check for unauthorized SMB connections to the Domain Controller.

```spl
index=main dest_ip="192.168.50.5" dest_port=445
| stats count by src_ip
| sort -count
```

**Expected:** Domain-joined workstations. **Unexpected:** Kali Linux or unknown IPs.

---

## Exercise 6: Find Logon Events by Type

**Scenario:** Understand how users are authenticating.

```spl
index=main EventCode=4624
| stats count by Logon_Type
| sort -count
```

| Logon Type | Meaning | Concern Level |
|------------|---------|---------------|
| 2 | Interactive (console) | Normal |
| 3 | Network (SMB, share) | Normal, watch for volume |
| 5 | Service | Normal for service accounts |
| 7 | Unlock | Normal |
| 10 | Remote Desktop (RDP) | Watch for unauthorized |

---

## Exercise 7: Timeline of an Attack (Combining Failed + Successful Logins)

**Scenario:** Reconstruct an attack timeline from a specific IP.

```spl
index=main (EventCode=4625 OR EventCode=4624) Source_Network_Address="192.168.50.30"
| eval Status=if(EventCode=4625, "FAILED", "SUCCESS")
| table _time, Status, Account_Name, Logon_Type
| sort _time
```

**What to present:** "At 10:15 AM, we observed 10 failed logins from 192.168.50.30 across 5 accounts. At 10:16 AM, the j.smith account successfully authenticated. This indicates a password spray with one successful credential compromise."

---

## Exercise 8: Detect Kerberoasting Attempts

**Scenario:** Find TGS ticket requests using weak encryption.

```spl
index=main EventCode=4769 Ticket_Encryption_Type=0x17
  Service_Name!="krbtgt" Service_Name!="*$"
| table _time, Account_Name, Service_Name, Client_Address
| sort -_time
```

**Why 0x17?** Encryption type 0x17 = RC4, which is crackable offline. Legitimate Kerberos uses AES (0x12).

---

## Exercise 9: Find All Admin Logons (Special Privileges)

**Scenario:** Monitor for unauthorized admin activity.

```spl
index=main EventCode=4672
| stats count by Account_Name
| sort -count
```

**Follow-up:** Check if the admin account logged in from an unexpected source:

```spl
index=main EventCode=4672 Account_Name="s.admin"
| table _time, Source_Network_Address, Logon_Type
```

---

## Exercise 10: Build a Summary Dashboard Query

**Scenario:** Create a single-pane overview for the SOC dashboard.

```spl
index=main (EventCode=4625 OR EventCode=4624 OR EventCode=4769 OR EventCode=4672)
| eval Category=case(
    EventCode=4625, "Failed Login",
    EventCode=4624, "Successful Login",
    EventCode=4769, "Kerberos TGS Request",
    EventCode=4672, "Admin Logon")
| stats count by Category
| sort -count
```

**What this gives you:** A quick health check — if "Failed Login" count suddenly spikes, investigate immediately.

---

## Interview Tips

When answering SPL questions in interviews:

1. **Start simple** — `index=main EventCode=4625 | stats count`
2. **Add context** — `| stats count by src_ip, Account_Name`
3. **Filter noise** — `| where count > 5`
4. **Present clearly** — `| table _time, Account_Name, src_ip | sort -_time`
5. **Explain your reasoning** — "I'm looking for repeated failures from the same IP because that's consistent with a brute force pattern"

---

*These exercises are part of a cybersecurity home lab portfolio demonstrating Tier 1 SOC Analyst skills.*
