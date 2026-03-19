# Hands-On SOC Analyst Lab Walkthrough

**Purpose:** Boot up your VMs, run real attacks, detect them in Splunk, triage alerts, and screenshot everything — so you can prove to interviewers that you've done this for real.

---

## Before You Start

### Boot Order (important — DC must come first)

| Order | VM | Why First |
|-------|----|-----------|
| 1 | **Windows Server 2022 (DC01)** | DNS + AD must be running first |
| 2 | **Ubuntu Server (Splunk)** | SIEM must be ready to receive logs |
| 3 | **Windows 11** | Needs DC for DNS resolution |
| 4 | **Kali Linux** | Attack machine — start last |

### Verify Everything Is Working

After all VMs are up (~5 minutes), run these checks:

**On Kali:**

```bash
ping -c 3 192.168.50.5    # DC01
ping -c 3 192.168.50.10   # Splunk
ping -c 3 192.168.50.20   # Win11
```

📸 **Screenshot: Kali pinging all hosts successfully**

**On your host (Garuda Linux) browser:**

- Open `http://192.168.50.10:8000`
- Login to Splunk (admin / your password)
- Go to **Search & Reporting**
- Run: `index=main | stats count by host` — you should see DC01 and WINDOWS

📸 **Screenshot: Splunk showing hosts and event counts**

> If DC01 doesn't show up, go to DC01 → open Services → find "SplunkForwarder" → make sure it's **Running**. If it's stopped, right-click → Start.

---

## Lab Exercise 1: Password Spray Attack + Detection

### Step 1: Run the Attack (Kali)

Open a terminal on Kali and run each command one at a time:

```bash
crackmapexec smb 192.168.50.5 -u 'j.smith' -p 'Password123!' -d cybersec.local
```

Wait 2 seconds, then:

```bash
crackmapexec smb 192.168.50.5 -u 'j.doe' -p 'Password123!' -d cybersec.local
```

Wait 2 seconds, then:

```bash
crackmapexec smb 192.168.50.5 -u 'b.wilson' -p 'Password123!' -d cybersec.local
```

Wait 2 seconds, then:

```bash
crackmapexec smb 192.168.50.5 -u 'svc_sql' -p 'Password123!' -d cybersec.local
```

Wait 2 seconds, then:

```bash
crackmapexec smb 192.168.50.5 -u 's.admin' -p 'Password123!' -d cybersec.local
```

📸 **Screenshot: Kali terminal showing all 5 CrackMapExec results (1 green SUCCESS, 4 red FAILED)**

Save as: `Screenshots/Kali_Linux/AD_Attacks/Kali_password_spray_live.png`

---

### Step 2: Detect in Splunk (Browser)

Wait 30 seconds for logs to arrive, then go to Splunk Search & Reporting.

**Query 1 — See all failed logins:**

```spl
index=main EventCode=4625 earliest=-15m
| table _time, Account_Name, Source_Network_Address, Failure_Reason
| sort -_time
```

📸 **Screenshot: Splunk table showing failed logins with 192.168.50.30 as source**

Save as: `Screenshots/Splunk/Splunk_password_spray_failed_logins.png`

**Query 2 — Check if any login succeeded:**

```spl
index=main (EventCode=4625 OR EventCode=4624) Source_Network_Address="192.168.50.30" earliest=-15m
| eval Status=if(EventCode==4625, "FAILED", "SUCCESS")
| table _time, Status, Account_Name, Source_Network_Address
| sort _time
```

📸 **Screenshot: Splunk showing FAILED/SUCCESS timeline — this proves you can correlate attacks**

Save as: `Screenshots/Splunk/Splunk_password_spray_timeline.png`

**Query 3 — Count by account:**

```spl
index=main EventCode=4625 Source_Network_Address="192.168.50.30" earliest=-15m
| stats count by Account_Name
| sort -count
```

📸 **Screenshot: Splunk bar chart or table showing failure count per account**

Save as: `Screenshots/Splunk/Splunk_password_spray_by_account.png`

---

### Step 3: Triage Decision

Write down your triage (you can put this in your own notes for interview prep):

> **Verdict:** True Positive — Password spray attack  
> **Evidence:** 4+ failed logins from single IP (192.168.50.30) across multiple accounts within 2 minutes  
> **Action:** Escalate — j.smith login succeeded, credential compromised  
> **SPL used:** EventCode 4625 + 4624 correlated by Source_Network_Address

---

## Lab Exercise 2: Kerberoasting + Detection

### Step 1: Sync Time (Kali)

```bash
sudo ntpdate 192.168.50.5
```

📸 **Screenshot: ntpdate output showing clock sync**

### Step 2: Run Kerberoasting (Kali)

```bash
impacket-GetUserSPNs 'cybersec.local/j.smith:Password123!' -dc-ip 192.168.50.5 -request
```

📸 **Screenshot: Kali showing either the TGS hash OR the clock skew error — both are good for your portfolio**

Save as: `Screenshots/Kali_Linux/AD_Attacks/Kali_kerberoasting_live.png`

### Step 3: Detect in Splunk (Browser)

```spl
index=main EventCode=4769 earliest=-15m
| table _time, Account_Name, Service_Name, Client_Address, Ticket_Encryption_Type
| sort -_time
```

📸 **Screenshot: Splunk showing the TGS request event — look for Encryption Type 0x17 (RC4)**

Save as: `Screenshots/Splunk/Splunk_kerberoasting_detection.png`

### Step 3b: If No EventCode 4769 Appears

If the Kerberoasting failed due to clock skew, you can still screenshot:

- The clock skew error from Kali (proves you attempted the attack)
- The Splunk query showing "no results" (proves you know what to look for)
- Your triage note explaining the situation

This is **still valuable** — interviewers appreciate honesty about lab issues.

---

## Lab Exercise 3: Nmap Scan + Detection

### Step 1: Run Nmap (Kali)

```bash
nmap -sT -p 1-1000 192.168.50.20
```

📸 **Screenshot: Nmap results showing open ports on Win11**

Save as: `Screenshots/Kali_Linux/AD_Attacks/Kali_nmap_win11_live.png`

### Step 2: Detect in Splunk

```spl
index=main src_ip="192.168.50.30" dest_ip="192.168.50.20" earliest=-15m
| stats dc(dest_port) as unique_ports, count as total_connections
```

📸 **Screenshot: Splunk showing 1000 unique ports from one IP — port scan confirmed**

Save as: `Screenshots/Splunk/Splunk_nmap_detection.png`

---

## Lab Exercise 4: Enum4linux Enumeration

### Step 1: Run Enum4linux (Kali)

```bash
enum4linux -a 192.168.50.5
```

📸 **Screenshot: enum4linux output showing domain info, users, shares**

Save as: `Screenshots/Kali_Linux/AD_Attacks/Kali_enum4linux_dc01.png`

### Step 2: Detect in Splunk

```spl
index=main EventCode=4662 earliest=-15m
| stats count by Account_Name, Object_Name
| sort -count
```

📸 **Screenshot: Splunk showing LDAP query events from the enumeration**

Save as: `Screenshots/Splunk/Splunk_enum4linux_detection.png`

---

## Lab Exercise 5: SOC Dashboard Review

### Step 1: Open Your Dashboard

Go to Splunk → Dashboards → **SOC Analyst Dashboard**

📸 **Screenshot: Full dashboard with all 5 panels showing data from today's attacks**

Save as: `Screenshots/Splunk/Splunk_SOC_dashboard_live.png`

---

## Lab Exercise 6: Check Alerts

### Step 1: View Triggered Alerts

Go to Splunk → Activity → **Triggered Alerts**

📸 **Screenshot: List of alerts that fired from your attacks — Brute Force, Port Scan, etc.**

Save as: `Screenshots/Splunk/Splunk_triggered_alerts.png`

---

## Summary of Screenshots to Take

| # | Screenshot | Location |
|---|-----------|----------|
| 1 | Kali pinging all hosts | Kali terminal |
| 2 | Splunk host count | Splunk Search |
| 3 | Password spray output | Kali terminal |
| 4 | Failed logins table | Splunk Search |
| 5 | Attack timeline (FAIL/SUCCESS) | Splunk Search |
| 6 | Failures by account | Splunk Search |
| 7 | ntpdate sync | Kali terminal |
| 8 | Kerberoasting attempt | Kali terminal |
| 9 | TGS request detection | Splunk Search |
| 10 | Nmap scan output | Kali terminal |
| 11 | Nmap detection in Splunk | Splunk Search |
| 12 | Enum4linux output | Kali terminal |
| 13 | Enum4linux detection | Splunk Search |
| 14 | SOC Dashboard with data | Splunk Dashboard |
| 15 | Triggered alerts list | Splunk Activity |

---

## Interview Prep: What to Say

When they ask *"walk me through how you'd investigate a brute force alert"*:

> "I'd start by looking at EventCode 4625 in Splunk, filtering by the source IP in the alert. I'd check how many accounts were targeted — if it's one account with many failures, it's a brute force; if it's many accounts with the same password, it's a spray. Then I'd immediately check EventCode 4624 from the same source IP to see if any login succeeded. If it did, that's a credential compromise — I'd escalate to Tier 2, document the IOCs, and recommend an immediate password reset."

When they ask *"have you used Splunk?"*:

> "Yes — I built a home lab with Splunk Enterprise, configured Universal Forwarders on a Windows 11 workstation and a Windows Server 2022 Domain Controller, created a SOC dashboard with 5 panels, set up 4 real-time alerts, and practiced triage on 10+ alerts from real attack simulations."

---

*Boot up your VMs when you're ready and start from the top. Take your time with each exercise — quality screenshots matter more than speed. 🚀*
