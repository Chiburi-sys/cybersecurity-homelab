# VM IP Address Map

This document lists all virtual machines in the cybersecurity home lab along with their assigned static IP addresses, operating systems, and primary roles. These mappings ensure consistent log ingestion, Splunk indexing, and reliable communication between systems during attack simulations.

---

## 🧭 Overview

All VMs are configured with **static IP addresses** on the VirtualBox **Internal Network (LabNet)** to maintain predictable connectivity and accurate log correlation.

- **Network:** LabNet  
- **Subnet:** 192.168.50.0/24  
- **Gateway:** 192.168.50.1  
- **DNS:** Local or default  
- **Purpose:** SIEM ingestion, attack simulation, detection engineering

---

## 🗂️ VM IP Address Table

| Hostname        | Role               | Operating System | Static IP         | Notes |
|-----------------|--------------------|------------------|-------------------|-------|
| UbuntuServer    | Splunk SIEM        | Ubuntu Server    | 192.168.50.10     | Hosts Splunk Enterprise; receives logs from Windows |
| Win11           | Workstation        | Windows 11       | 192.168.50.20     | Sysmon installed; sends logs to Splunk Forwarder |
| Kali            | Attack Machine     | Kali Linux       | 192.168.50.30     | Used for offensive security tasks and simulations |

---

## 🔧 Configuration Notes

### Ubuntu Server (Splunk SIEM)
- Static IP set via Netplan  
- Receives logs from Windows 11  
- Runs Splunk Enterprise for indexing and detection  

### Windows 11 Workstation
- Static IP set via GUI  
- Sysmon installed for endpoint telemetry  
- Universal Forwarder sends logs to Splunk  

### Kali Linux
- Static IP set via `/etc/network/interfaces` or NetworkManager  
- Used for brute force, malware execution, and web app attacks  
- **Static IP:** 192.168.50.30  
- **Subnet Mask:** 255.255.255.0  
- **Gateway:** 192.168.50.1  
- **DNS Server:** 8.8.8.8  
- **DHCP:** Disabled  
- **Adapter:** Intel PRO/1000 MT (Internal Network: LabNet)  
- **Verification:** `ip a` output confirms static assignment


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
