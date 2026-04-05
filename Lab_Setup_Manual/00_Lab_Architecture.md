# Lab Network Diagram
This document outlines the internal network architecture of the cybersecurity home lab used for attack simulation, SIEM deployment, Active Directory, and detection engineering.
---
## 🧠 Overview
- **Virtualization Platform:** VirtualBox  
- **Host OS:** Garuda Linux (KDE Plasma)  
- **Network Type:** Internal Network (LabNet)  
- **Subnet:** 192.168.50.0/24  
- **Gateway:** 192.168.50.1  
- **Domain:** cybersec.local  
- **DNS:** 192.168.50.5 (Domain Controller)
All VMs are configured with static IPs to ensure consistent log correlation and Splunk ingestion.
---
## 🗺️ ASCII Diagram  
**Internal VirtualBox Network Topology**
```
                            ┌──────────────────────────┐
                            │      VirtualBox Host     │
                            │    Garuda Linux (KDE)    │
                            └────────────┬─────────────┘
                                         │
                              Internal Network: LabNet
                              Subnet: 192.168.50.0/24
                              Domain: cybersec.local
                                         │
         ┌───────────────┬───────────────┼───────────────┬
         │               │               │               │               
┌────────┴───────┐ ┌─────┴──────┐ ┌──────┴──────┐  ┌─────┴──────┐
│ Windows Server │ │ Ubuntu     │ │ Windows 11  │  │ Kali Linux │
│ 2022 (DC01)    │ │ Server     │ │ Workstation │  │ Attacker   │
│ AD DS / DNS    │ │ Splunk SIEM│ │ Sysmon +    │  │ Nmap, CME  │
│                │ │            │ │ Forwarder   │  │ Responder  │
│ 192.168.50.5   │ │ .50.10     │ │ .50.20      │  │ .50.30     │
└────────┬───────┘ └─────┬──────┘ └──────┬──────┘  └────────────┘
         │               │               │
         │  Logs (9997)  │  Logs (9997)  │
         └───────────────┴───────────────┘
                         │
              ┌──────────┴──────────┐
              │   Splunk Enterprise │
              │   Ubuntu Server     │
              │   192.168.50.10     │
              └─────────────────────┘
```
---
## 🧾 Host Table
| Host                | Role                 | IP Address      | OS                            | Services                    |
|---------------------|----------------------|-----------------|-------------------------------|-----------------------------|
| Windows Server 2022 | Domain Controller    | 192.168.50.5    | Windows Server 2022 Standard  | AD DS, DNS, Splunk Forwarder|
| Ubuntu Server       | Splunk SIEM          | 192.168.50.10   | Ubuntu Server                 | Splunk Enterprise (port 8000, 9997) |
| Windows 11          | Domain Workstation   | 192.168.50.20   | Windows 11                    | Sysmon, Splunk Forwarder    |
| Kali Linux          | Attack Machine       | 192.168.50.30   | Kali Linux                    | Nmap, CrackMapExec, Responder |
---
## 🔍 Purpose of Each Node
- **Windows Server 2022 (DC01)**  
  Domain Controller running Active Directory Domain Services and DNS. Hosts the `cybersec.local` domain. Sends AD authentication, Directory Service, and DNS logs to Splunk.
- **Ubuntu Server**  
  Hosts Splunk Enterprise. Receives logs from both Windows hosts via Universal Forwarder on port 9997. Provides dashboards, alerts, and search capabilities.
- **Windows 11**  
  Domain-joined workstation configured with Sysmon for endpoint telemetry. Primary target for attack simulations. Sends Security, Sysmon, Application, and System logs to Splunk.
- **Kali Linux**  
  Used for offensive security tasks including brute force, port scanning, AD attacks (Kerberoasting, LLMNR poisoning), and enumeration.
---
## 🛡️ Use Cases Supported
- SIEM deployment and log ingestion  
- Active Directory attack and defense  
- Attack simulation and telemetry generation  
- Detection engineering and SPL query development  
- Incident response and documentation  
- Screenshots for portfolio evidence
---
## 🧩 Notes
- All systems use static IPs for consistent Splunk indexing  
- Network is isolated from the internet for safe testing  
- VirtualBox NAT is disabled to prevent external traffic  
- Windows 11 DNS points to DC (192.168.50.5) for domain resolution  
- Screenshots of IP configs are stored in `Screenshots/`
---
## 📁 Related Files
- [`01_IP_Address_Map.md`](01_IP_Address_Map.md) — Static IP assignments  
- `virtualbox_interface.png` — Network adapter settings  
- `Screenshots/` — OS-specific configuration screenshots
---
## 🧪 Verification
- Windows Server 2022 can ping Ubuntu Server ✅  
- Windows 11 can ping Ubuntu Server ✅  
- Windows 11 can ping Domain Controller ✅  
- Kali Linux can ping all hosts ✅  
- All IPs aligned within `192.168.50.0/24` subnet ✅  
- Windows 11 joined to `cybersec.local` domain ✅
