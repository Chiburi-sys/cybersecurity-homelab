# VM IP Address Map
This document lists all virtual machines in the cybersecurity home lab along with their assigned static IP addresses, operating systems, and primary roles.
---
## 🧭 Overview
All VMs are configured with **static IP addresses** on the VirtualBox **Internal Network (LabNet)**.
- **Network:** LabNet  
- **Subnet:** 192.168.50.0/24  
- **Gateway:** 192.168.50.1  
- **Domain:** cybersec.local  
- **DNS:** 192.168.50.5 (Domain Controller)  
- **Purpose:** SIEM ingestion, AD attack simulation, detection engineering
---
## 🗂️ VM IP Address Table
| Hostname           | Role                | Operating System              | Static IP       | Notes |
|--------------------|---------------------|-------------------------------|-----------------|-------|
| DC01               | Domain Controller   | Windows Server 2022 Standard  | 192.168.50.5    | AD DS, DNS; sends logs to Splunk |
| UbuntuServer       | Splunk SIEM         | Ubuntu Server                 | 192.168.50.10   | Hosts Splunk Enterprise; receives logs |
| Win11              | Domain Workstation  | Windows 11                    | 192.168.50.20   | Sysmon installed; domain-joined |
| Kali               | Attack Machine      | Kali Linux                    | 192.168.50.30   | Offensive security simulations |
---
## 🔧 Configuration Notes
### Windows Server 2022 (Domain Controller — DC01)
- Static IP set via Server Manager → Local Server → Ethernet  
- Promoted to Domain Controller for `cybersec.local`  
- Runs AD DS and DNS services  
- Splunk Universal Forwarder sends AD, DNS, and Security logs  
### Ubuntu Server (Splunk SIEM)
- Static IP set via Netplan  
- Receives logs from Windows Server and Windows 11  
- Runs Splunk Enterprise for indexing and detection  
### Windows 11 Workstation
- Static IP set via GUI  
- DNS set to 192.168.50.5 (Domain Controller)  
- Joined to `cybersec.local` domain  
- Sysmon installed for endpoint telemetry  
- Universal Forwarder sends logs to Splunk  
### Kali Linux
- Static IP set via NetworkManager  
- Used for brute force, port scanning, AD attacks, and enumeration  
- **Static IP:** 192.168.50.30  
- **Subnet Mask:** 255.255.255.0  
- **Gateway:** 192.168.50.1  
- **DNS Server:** 8.8.8.8  
- **Adapter:** Intel PRO/1000 MT (Internal Network: LabNet)
---
## 📁 Related Files
- `network_diagram.md` — Visual network layout  
- `virtualbox_interface.png` — Adapter configuration  
- `Screenshots/` — OS-specific IP configuration screenshots  
---
## 📝 Purpose
This file provides a quick reference for:
- Troubleshooting connectivity  
- Writing Splunk queries  
- Correlating logs across systems  
- Documenting the lab environment for your portfolio  
Consistent IP mapping is essential for SIEM accuracy, detection engineering, and repeatable attack simulations.
