# SOC Playbook — Kerberoasting Attack Response

**Playbook ID:** PB-003  
**Author:** Stacy Bostick  
**Last Updated:** 2026-03-01  
**Severity:** Critical  
**MITRE ATT&CK:** T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting

---

## 1. Detection

### Trigger Conditions

- Multiple Kerberos TGS ticket requests (EventCode 4769) with encryption type 0x17 (RC4)
- Requests for service tickets from a single user in a short time frame
- Ticket requests for accounts with SPNs that are not machine accounts

### Detection Query

```spl
index=main EventCode=4769 Ticket_Encryption_Type=0x17 Service_Name!="krbtgt" Service_Name!="*$"
| stats count by Client_Address, Service_Name, Account_Name
| where count > 3
| sort -count
```

### Alternative Detection — Anomalous TGS Requests

```spl
index=main EventCode=4769
| stats dc(Service_Name) as unique_services, count by Account_Name, Client_Address
| where unique_services > 5
| sort -unique_services
```

---

## 2. Triage (First 5 Minutes)

### Step 1: Identify the Requesting Account

- [ ] Which user account requested the service tickets?
- [ ] Is this a normal user or a service account?
- [ ] When did the requests occur? (Bulk requests = automated tool)

### Step 2: Check the Targeted SPNs

```spl
index=main EventCode=4769 Account_Name="<SUSPICIOUS_USER>"
| table _time, Service_Name, Client_Address, Ticket_Encryption_Type
| sort _time
```

- [ ] Which service accounts were targeted?
- [ ] Were these requests made with RC4 encryption (0x17)? RC4 = easier to crack

### Step 3: Assess the Risk

- [ ] Do the targeted service accounts have admin privileges?
- [ ] Are they using weak/old passwords?
- [ ] When were the passwords last changed?

```powershell
# Run on DC to check password age
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties PasswordLastSet, ServicePrincipalName | Select-Object Name, SamAccountName, PasswordLastSet
```

---

## 3. Investigation (Next 15 Minutes)

### Step 4: Check for Successful Authentication

```spl
index=main EventCode=4624 Account_Name="<SERVICE_ACCOUNT>"
| table _time, Account_Name, Workstation_Name, LogonType, Source_Network_Address
| sort -_time
```

- [ ] Has anyone logged in as the service account after the Kerberoasting attempt?
- [ ] Any logon from unusual workstations or IPs?

### Step 5: Look for Attack Tools

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  (CommandLine="*GetUserSPNs*" OR CommandLine="*Invoke-Kerberoast*"
   OR CommandLine="*Rubeus*" OR CommandLine="*kerberoast*")
| table _time, User, Image, CommandLine
```

### Step 6: Check for Lateral Movement Post-Compromise

```spl
index=main EventCode=4624 LogonType=3 Account_Name="<SERVICE_ACCOUNT>"
| stats count by Workstation_Name
| sort -count
```

---

## 4. Containment

### Immediate Actions

- [ ] Reset the password of ALL targeted service accounts immediately
- [ ] Use strong passwords (25+ characters, randomly generated)
- [ ] Disable the requesting user account if compromised
- [ ] Review the service account permissions and reduce if possible

---

## 5. Remediation

### Short-Term

- [ ] Rotate all service account passwords
- [ ] Convert service accounts to Group Managed Service Accounts (gMSA) where possible
- [ ] Remove unnecessary SPNs from accounts
- [ ] Enforce AES encryption for Kerberos (disable RC4 if possible)

### Long-Term

- [ ] Implement a service account password rotation policy (90 days max)
- [ ] Monitor EventCode 4769 with RC4 encryption as an ongoing alert
- [ ] Audit all accounts with SPNs regularly
- [ ] Consider implementing Privileged Access Management (PAM)

---

## 6. Tools Used in Kerberoasting

| Tool | Platform | Description |
|---|---|---|
| impacket-GetUserSPNs | Linux/Kali | Python-based SPN enumeration and TGS request |
| Rubeus | Windows | C# Kerberos abuse toolkit |
| Invoke-Kerberoast | PowerShell | PowerSploit module for Kerberoasting |
| hashcat | Linux/Windows | Offline hash cracking (mode 13100 for Kerberos) |
| John the Ripper | Linux | Alternative offline hash cracker |

---

## 7. Key Event Codes for AD Attacks

| EventCode | Description | Relevance |
|---|---|---|
| 4768 | TGT Request (AS-REQ) | Kerberos authentication initiation |
| 4769 | TGS Request (Service Ticket) | **Kerberoasting indicator** |
| 4771 | Pre-Auth Failed | AS-REP Roasting indicator |
| 4625 | Failed Logon | Brute force / password spray |
| 4624 | Successful Logon | Post-compromise verification |
| 4672 | Special Privileges Assigned | Admin logon detection |
