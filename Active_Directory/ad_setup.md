# Active Directory Lab Setup Guide
**Date:** 2026-02-28
**Analyst:** Stacy
**Environment:** VirtualBox Home Lab
**Domain Name:** cybersec.local
---
## Overview
This document covers the complete setup of an Active Directory Domain Services (AD DS) environment using Windows Server 2022 as a Domain Controller. The domain is used for simulating enterprise authentication, group policy, and AD-based attack scenarios for SOC analyst training.
---
## Prerequisites
| Component            | Detail                                              |
|----------------------|-----------------------------------------------------|
| VM                   | Windows Server 2022 Standard Evaluation (Desktop)   |
| RAM                  | 4096 MB                                             |
| CPU                  | 2 cores                                             |
| Disk                 | 50 GB                                               |
| Network              | Internal Network (LabNet)                           |
| Static IP            | 192.168.50.5                                        |
| Administrator Pass   | P@ssw0rd123!                                        |
---
## Step 1: Set Static IP Address
1. Open **Server Manager** → Click **Local Server**
2. Click on **Ethernet** (next to the IP address)
3. Right-click the adapter → **Properties**
4. Double-click **Internet Protocol Version 4 (TCP/IPv4)**
5. Set:
| Setting        | Value           |
|----------------|-----------------|
| IP Address     | 192.168.50.5    |
| Subnet Mask    | 255.255.255.0   |
| Default Gateway| 192.168.50.1    |
| Preferred DNS  | 127.0.0.1       |
1. Click **OK** → **Close**
---
## Step 2: Rename the Server
1. Open **Server Manager** → **Local Server**
2. Click **Computer name**
3. Click **Change**
4. Set Computer name to: `DC01`
5. Click **OK** → **Restart Now**
---
## Step 3: Install Active Directory Domain Services
1. Open **Server Manager** → Click **Manage → Add Roles and Features**
2. Click **Next** through the wizard until "Server Roles"
3. Check **Active Directory Domain Services**
4. Click **Add Features** when prompted
5. Click **Next** through remaining screens → **Install**
6. Wait for installation to complete
---
## Step 4: Promote to Domain Controller
1. In Server Manager, click the **flag notification** → **Promote this server to a domain controller**
2. Select **Add a new forest**
3. Root domain name: `cybersec.local`
4. Click **Next**
5. Set **DSRM Password**: `P@ssw0rd123!`
6. Click **Next** through all remaining screens (accept defaults)
7. Click **Install**
8. The server will automatically restart
---
## Step 5: Create Organizational Units (OUs)
After restart, open **Active Directory Users and Computers** (from Server Manager → Tools):
1. Right-click `cybersec.local` → **New → Organizational Unit**
2. Create the following OUs:
| OU Name      | Purpose                          |
|--------------|----------------------------------|
| IT           | IT department user accounts      |
| HR           | Human Resources accounts         |
| Finance      | Finance department accounts      |
| Workstations | Domain-joined computer accounts  |
---
## Step 6: Create Domain Users
In Active Directory Users and Computers:
1. Right-click the **IT** OU → **New → User**
2. Create these accounts:
| Full Name      | Username    | Password        | OU      | Groups         |
|----------------|-------------|-----------------|---------|----------------|
| Stacy Admin    | s.admin     | CyberAdmin1!    | IT      | Domain Admins  |
| John Smith     | j.smith     | Password123!    | IT      | Domain Users   |
| Jane Doe       | j.doe       | Welcome2026!    | HR      | Domain Users   |
| Bob Wilson     | b.wilson    | Finance2026!    | Finance | Domain Users   |
| SQL Service    | svc_sql     | SQLService1!    | IT      | Domain Users   |
> **Note:** `svc_sql` uses a weak password intentionally — this account will be the target for Kerberoasting attacks.
1. For each user, uncheck **"User must change password at next logon"**
---
## Step 7: Configure Service Principal Name (SPN) for Kerberoasting
Open **PowerShell as Administrator** on the Domain Controller:
```powershell
setspn -a DC01/svc_sql.cybersec.local:60111 cybersec\svc_sql
```
This registers an SPN on the `svc_sql` account, making it vulnerable to Kerberoasting — a common AD attack technique.
---
## Step 8: Join Windows 11 to the Domain
On the **Windows 11 VM**:
1. Change DNS to point to the Domain Controller:
   - Open Network Settings → Change adapter options
   - Right-click Ethernet → Properties → IPv4
   - Set **Preferred DNS** to `192.168.50.5` (the DC)
2. Join the domain:
   - Right-click **This PC** → Properties → **Rename this PC (advanced)**
   - Click **Change** → Select **Domain** → Enter: `cybersec.local`
   - When prompted, enter credentials: `cybersec\s.admin` / `CyberAdmin1!`
3. Restart Windows 11
4. Log in with a domain account (e.g., `cybersec\j.smith`)
---
## Step 9: Install Splunk Universal Forwarder on Windows Server
1. Download the Splunk Universal Forwarder on the DC (same method as Windows 11)
2. Configure `outputs.conf`:
```ini
[tcpout]
defaultGroup = default-autolb-group
[tcpout:default-autolb-group]
server = 192.168.50.10:9997
```
1. Configure `inputs.conf`:
```ini
[WinEventLog://Application]
disabled = 0
index = main
[WinEventLog://Security]
disabled = 0
index = main
[WinEventLog://System]
disabled = 0
index = main
[WinEventLog://Directory Service]
disabled = 0
index = main
[WinEventLog://DNS Server]
disabled = 0
index = main
[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = main
renderXml = true
```
1. Restart the SplunkForwarder service
---
## Step 10: AD Attack Simulations from Kali
### Kerberoasting
```bash
impacket-GetUserSPNs cybersec.local/j.smith:Password123! -dc-ip 192.168.50.5 -request
```
### LLMNR/NBT-NS Poisoning
```bash
sudo responder -I eth0
```
### Password Spraying
```bash
crackmapexec smb 192.168.50.5 -u users.txt -p "Password123!" -d cybersec.local
```
### Enumeration with BloodHound
```bash
bloodhound-python -u j.smith -p 'Password123!' -d cybersec.local -ns 192.168.50.5 -c All
```
---
## Verification Checklist
- [ ] Windows Server has static IP 192.168.50.5
- [ ] Server renamed to DC01
- [ ] AD DS role installed and server promoted
- [ ] Domain `cybersec.local` is operational
- [ ] OUs created (IT, HR, Finance, Workstations)
- [ ] User accounts created with appropriate group memberships
- [ ] SPN set on svc_sql for Kerberoasting lab
- [ ] Windows 11 joined to the domain
- [ ] Splunk Forwarder on DC sending logs
- [ ] Kali can reach the DC (ping 192.168.50.5)
---
*This setup guide is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
