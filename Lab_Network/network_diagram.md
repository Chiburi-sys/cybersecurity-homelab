# Lab Network Diagram

This document outlines the internal network architecture of the cybersecurity home lab used for attack simulation, SIEM deployment, and detection engineering.

---

## 🧠 Overview

- **Virtualization Platform:** VirtualBox  
- **Host OS:** Garuda Linux (KDE Plasma)  
- **Network Type:** Internal Network (LabNet)  
- **Subnet:** 192.168.50.0/24  
- **Gateway:** 192.168.50.1  
- **DNS:** Local or default

All VMs are configured with static IPs to ensure consistent log correlation and Splunk ingestion.

---

## 🗺️ ASCII Diagram  
**Internal VirtualBox Network Topology**

                            ┌──────────────────────────┐
                            │      VirtualBox Host     │
                            │  Garuda Linux (KDE)      │
                            └─────────────┬────────────┘
                                          │
                               Internal Network: LabNet
                               Subnet: 192.168.50.0/24
                                          │
                          ┌───────────────┼────────────────────────┐
                          │               │                        │
                          │               │                        │
              ┌──────────────┐      ┌────────────────┐       ┌────────────────┐
              │ UbuntuServer  │      │ Windows 11     │       │ Kali Linux      │
              │ Splunk SIEM   │      │ Workstation    │       │ Attack Machine  │
              │ IP: 192.168.50.10 │  │ IP: 192.168.50.20 │   │ IP: 192.168.50.30 │
              │ GW: 192.168.50.1  │  │ GW: 192.168.50.1  │   │ GW: 192.168.50.1  │
              └──────────────┘      └────────────────┘       └────────────────┘



---

## 🧾 Host Table

| Host            | Role              | IP Address         | OS                 |
|-----------------|-------------------|--------------------|-------------------|
| Ubuntu Server   | Splunk SIEM       | 192.168.50.10      | Ubuntu Server     |
| Windows 11      | Workstation       | 192.168.50.20      | Windows 11        |
| Kali Linux      | Attack Machine    | 192.168.50.30      | Kali Linux        |

---

## 🔍 Purpose of Each Node

- **Ubuntu Server**  
  Hosts Splunk Enterprise and Universal Forwarder. Receives logs from Windows and parses Sysmon events.

- **Windows 11**  
  Configured with Sysmon for endpoint telemetry. Used for attack simulation targets and detection testing.

- **Kali Linux**  
  Used for offensive security tasks including brute force, malware execution, and web app exploitation.

---

## 🛡️ Use Cases Supported

- SIEM deployment and log ingestion  
- Attack simulation and telemetry generation  
- Detection engineering and SPL query development  
- Incident response and documentation  
- Screenshots for portfolio evidence

---

## 🧩 Notes

- All systems use static IPs for consistent Splunk indexing  
- Network is isolated from the internet for safe testing  
- VirtualBox NAT is disabled to prevent external traffic  
- Screenshots of IP configs are stored in `Screenshots/`

---

## 📁 Related Files

- `vm_ip_map.md` — Static IP assignments  
- `virtualbox_interface.png` — Network adapter settings  
- `Screenshots/` — OS-specific configuration screenshots


## 🧪 Verification

- Windows 11 can ping Ubuntu Server  
- Kali Linux can ping Ubuntu Server  
- Kali → Windows ping failed prior to static IP setup  
- All IPs now aligned within `192.168.50.0/24` subnet
