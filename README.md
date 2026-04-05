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
| `Lab_Setup_Manual/` | **Tutorial:** Step-by-step guides for the entire lab build |
| `Attack_Simulation/` | Nmap, CrackMapExec, password spraying, Kerberoasting |
| `Incident_Reports/` | SOC-style incident documentation and response playbooks |
| `Screenshots/` | Visual evidence organized by OS/tool |
| `Scripts/` | Python lab utilities (SIEM webhook helpers live under each SIEM folder) |
| `SOC_Analyst/` | Tier 1 SOC simulation — triage, tickets, escalation |
| `Splunk_SIEM/` | Splunk Enterprise setup, SPL queries, and SOC dashboards |
| `Wazuh_SIEM/` | Wazuh Manager (Docker) setup, custom XML rules, SOAR automation, and Rootkit detection |
| `Web_App_Pentesting/` | DVWA, Juice Shop findings |
| `Resume/` | Resume, cover letters, and application blurbs |

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
                    │    VirtualBox Host Admin  │
                    │    Garuda Linux (KDE)     │
                    │    + Docker (Wazuh Stack) │
                    └────────────┬─────────────┘
                                 │
                      Internal Network: LabNet
                      Subnet: 192.168.50.0/24
                                 │
      ┌────────────────┬─────────┴─────────┬────────────────┐
      │                │                   │                │
┌─────┴──────┐  ┌──────┴──────┐     ┌──────┴──────┐  ┌──────┴──────┐
│ DC01       │  │ Ubuntu      │     │ Win11       │  │ Kali        │
│ .50.5      │  │ .50.10      │     │ .50.20      │  │ .50.30      │
│ AD DS / DNS│  │ Splunk SIEM │     │ Sysmon +    │  │ Attacker    │
│ Forwarder  │  │ Indexer     │     │ Forwarder   │  │ Nmap / CME  │
└────────────┘  └─────────────┘     └─────────────┘  └─────────────┘
```

---

## 📎 Key Documents

- [`splunk_setup.md`](Lab_Setup_Manual/splunk_setup.md) — Splunk Linux installation  
- [`wazuh_setup.md`](Lab_Setup_Manual/wazuh_setup.md) — Wazuh Docker deployment  
- [**AD DS Setup Guide**](Lab_Setup_Manual/ad_setup_guide.md) — Domain controller setup  
- [**DVWA Setup Guide**](Lab_Setup_Manual/dvwa_setup_guide.md) — Web application target lab  
- [**Lab Architecture Diagram**](Lab_Setup_Manual/00_Lab_Architecture.md) — Full lab topology  
- [**IP Address Map**](Lab_Setup_Manual/01_IP_Address_Map.md) — Static IP assignments  
- [`wazuh_detection_engineering.md`](Wazuh_SIEM/wazuh_detection_engineering.md) — Wazuh rules & SOAR logic  
- [`vulnerability_assessment.md`](Wazuh_SIEM/vulnerability_assessment.md) — Wazuh Vulnerability reporting  
- [`rootkit_anomaly_detection.md`](Wazuh_SIEM/rootkit_anomaly_detection.md) — Rootkit/Anomaly detection report  
- [`walkthrough_anomaly_tuning.md`](Wazuh_SIEM/walkthrough_anomaly_tuning.md) — Educational guide: SIEM Tuning & Forensic Triage  
- [`001_brute_force_smb.md`](Incident_Reports/001_brute_force_smb.md) — SMB brute force incident  
- [`002_ad_password_spray.md`](Incident_Reports/002_ad_password_spray.md) — AD password spray incident  
- [`002_wazuh_fim_alert.md`](Incident_Reports/002_wazuh_fim_alert.md) — Wazuh FIM alert incident  
- [`alert_triage_log.md`](SOC_Analyst/alert_triage_log.md) — Tier 1 shift: 10 alerts with TP/FP/benign verdicts and SPL  
- [`hands_on_lab_walkthrough.md`](SOC_Analyst/hands_on_lab_walkthrough.md) — Step-by-step SOC lab guide  
- [`Stacy_Bostick_Resume.md`](Resume/Stacy_Bostick_Resume.md) — Resume (Markdown)  
- [`resume_cover_letter_blurbs.md`](Resume/resume_cover_letter_blurbs.md) — Application blurbs and talking points  

---

## 📬 Contact

Connect on LinkedIn (see resume for profile link) or browse this project on [GitHub](https://github.com/Chiburi-sys/cybersecurity-homelab).

---

Thanks for visiting!
