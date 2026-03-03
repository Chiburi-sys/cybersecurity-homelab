# Updated Lab Network Diagram

## Overview

- **Virtualization Platform:** VirtualBox
- **Host OS:** Garuda Linux (KDE Plasma)
- **Network Type:** Internal Network (LabNet)
- **Subnet:** 192.168.50.0/24
- **Domain:** cybersec.local

---

## Network Topology

```
                            ┌──────────────────────────┐
                            │      VirtualBox Host      │
                            │    Garuda Linux (KDE)     │
                            └────────────┬─────────────┘
                                         │
                              Internal Network: LabNet
                              Subnet: 192.168.50.0/24
                              Domain: cybersec.local
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
    ┌─────────┴──────────┐    ┌─────────┴──────────┐    ┌─────────┴──────────┐
    │  Windows Server     │    │   Windows 11        │    │   Kali Linux        │
    │  Domain Controller  │    │   Domain Workstation │    │   Attack Machine    │
    │  AD DS / DNS        │    │   Sysmon + Forwarder │    │   Nmap / CME        │
    │  IP: 192.168.50.5   │    │   IP: 192.168.50.20  │    │   IP: 192.168.50.30 │
    └─────────┬──────────┘    └─────────┬──────────┘    └────────────────────┘
              │                          │
              │     Logs (port 9997)     │
              └──────────┬───────────────┘
                         │
              ┌──────────┴──────────┐
              │   Ubuntu Server      │
              │   Splunk SIEM        │
              │   IP: 192.168.50.10  │
              └─────────────────────┘
```

---

## Host Table

| Host               | Role                 | IP Address      | OS                             | Services |
|--------------------|----------------------|-----------------|--------------------------------|----------|
| Windows Server 2022| Domain Controller    | 192.168.50.5    | Windows Server 2022 Standard   | AD DS, DNS, DHCP |
| Ubuntu Server      | Splunk SIEM          | 192.168.50.10   | Ubuntu Server                  | Splunk Enterprise |
| Windows 11         | Domain Workstation   | 192.168.50.20   | Windows 11                     | Sysmon, Splunk Forwarder |
| Kali Linux         | Attack Machine       | 192.168.50.30   | Kali Linux                     | Nmap, CrackMapExec, Hydra |

---

## Data Flow

1. **Windows Server 2022** → Sends AD/DNS/Security logs → **Splunk (Ubuntu)**
2. **Windows 11** → Sends Sysmon + Security logs → **Splunk (Ubuntu)**
3. **Kali Linux** → Attacks Windows Server & Windows 11
4. **Splunk** → Ingests, correlates, alerts, and visualizes all events
