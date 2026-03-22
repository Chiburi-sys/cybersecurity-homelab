# Cybersecurity Portfolio — Stacy

Welcome to my cybersecurity home lab portfolio. This repository showcases hands-on projects, attack simulations, SIEM deployment, Active Directory security, and incident response documentation — all built in a fully virtualized lab environment.

---

## 🧠 Lab Overview

- **Host OS:** Garuda Linux (KDE Plasma)  
- **Virtualization:** VirtualBox  
- **Network:** Internal (LabNet, 192.168.50.0/24)  
- **Domain:** cybersec.local  
- **Domain Controller:** Windows Server 2022 (DC01)  
- **SIEM Pipeline 1 (Splunk):** Splunk Enterprise (Ubuntu Server) + Sysmon + Universal Forwarder  
- **SIEM Pipeline 2 (Wazuh):** Wazuh Manager/Indexer/Dashboard (Docker) + Wazuh Agent  
- **Attack Simulation:** Kali Linux

---

## 📁 Folder Structure

| Folder | Description |
|--------|-------------|
| `Active_Directory/` | AD DS setup, Kerberoasting attack, BloodHound analysis |
| `Attack_Simulation/` | Nmap, CrackMapExec, password spraying, Kerberoasting |
| `Incident_Reports/` | SOC-style incident documentation and response playbooks |
| `Lab_Network/` | Network diagram, IP map, topology |
| `Screenshots/` | Visual evidence organized by OS/tool |
| `Scripts/` | Python and PowerShell tools |
| `SOC_Analyst/` | Tier 1 SOC simulation — triage, tickets, escalation |
| `Splunk_SIEM/` | Splunk Enterprise setup, SPL queries, and SOC dashboards |
| `Wazuh_SIEM/` | Wazuh Manager (Docker) setup, custom XML rules, SOAR automation, and Rootkit detection |
| `Web_App_Pentesting/` | DVWA, Juice Shop findings |
| `Resume/` | Cybersecurity certificate |

---

## 🎯 Skills Demonstrated

- **SIEM Deployment** — Splunk Enterprise & Wazuh Manager (Docker) installation and configuration  
- **Active Directory** — Domain controller setup, user/group management, GPO basics  
- **Detection Engineering** — Custom SPL queries (Splunk), XML rules (Wazuh), and SOAR playbooks (Discord/Active Response)  
- **Attack Simulation** — Kerberoasting, password spraying, nmap, SMB brute force  
- **Incident Response** — SOC-style reports, playbooks, MITRE ATT&CK mapping  
- **Forensic Investigation** — Using system-native tools (`pacman`, `stat`, `shadow`) to triage and validate security anomalies  
- **Network Architecture** — 4-VM isolated lab + Dockerized SIEM with static IP topology  
- **Documentation** — Professional markdown docs with screenshots for GitHub

---

## 🖥️ Lab Topology

```
                    ┌──────────────────────────┐
                    │    VirtualBox Host        │
                    │    Garuda Linux (KDE)     │
                    │    + Docker (Wazuh)       │
                    └────────────┬─────────────┘
                                 │
                      Internal Network: LabNet
                      Subnet: 192.168.50.0/24
                                 │
     ┌───────────────┬───────────┼───────────┬───────────────┐
     │               │           │           │               │
┌────┴─────┐  ┌──────┴────┐ ┌───┴────┐  ┌───┴──────┐
│ DC01     │  │ Ubuntu    │ │ Win11  │  │ Kali     │
│ .50.5    │  │ .50.10    │ │ .50.20 │  │ .50.30   │
│ AD DS    │  │ Splunk    │ │ Sysmon │  │ Attacker │
└──────────┘  └───────────┘ └────────┘  └──────────┘
```

---

## 📎 Key Documents

- [`network_diagram.md`](Lab_Network/network_diagram.md) — Full lab topology  
- [`ad_setup_guide.md`](Active_Directory/ad_setup_guide.md) — Domain controller setup  
- [`kerberoasting.md`](Active_Directory/kerberoasting.md) — Kerberoasting attack & detection  
- [`ad_attacks.md`](Attack_Simulation/ad_attacks.md) — All AD attack simulations  
- [`spl_queries.md`](Splunk_SIEM/spl_queries.md) — Splunk detection queries  
- [`wazuh_setup.md`](Wazuh_SIEM/wazuh_setup.md) — Wazuh Docker deployment guide  
- [`wazuh_detection_engineering.md`](Wazuh_SIEM/wazuh_detection_engineering.md) — Wazuh rules & SOAR logic  
- [`vulnerability_assessment.md`](Wazuh_SIEM/vulnerability_assessment.md) — Wazuh Vulnerability reporting  
- [`rootkit_anomaly_detection.md`](Wazuh_SIEM/rootkit_anomaly_detection.md) — Rootkit/Anomaly detection report  
- [`001_brute_force_smb.md`](Incident_Reports/001_brute_force_smb.md) — SMB brute force incident  
- [`002_ad_password_spray.md`](Incident_Reports/002_ad_password_spray.md) — AD password spray incident  
- [`002_wazuh_fim_alert.md`](Incident_Reports/002_wazuh_fim_alert.md) — Wazuh FIM alert incident  
- [`hands_on_lab_walkthrough.md`](SOC_Analyst/hands_on_lab_walkthrough.md) — Step-by-step SOC lab guide  
- [`interview_prep.md`](interview_prep.md) — Conversational SOC analyst interview prep  

---

## 📬 Contact

Feel free to connect with me on [LinkedIn](https://www.linkedin.com/) or explore more projects on my [GitHub profile](https://github.com/).

---

Thanks for visiting!
