# Attack Simulation

This folder contains offensive security exercises performed in a controlled home lab environment using Kali Linux. These simulations generate telemetry for SIEM ingestion and incident response practice.

---

## Contents

### Completed

| File | Attack Type | MITRE ATT&CK |
|------|-------------|---------------|
| `nmap_port_scan.md` | Port scanning & enumeration | T1046 |
| `smb_brute_force.md` | SMB brute force (Win11) | T1110 |
| `brute_force_ssh.md` | SSH brute force (Ubuntu) | T1110.001 |
| `ad_attacks.md` | Kerberoasting + Password Spray + Enumeration | T1558.003, T1110.003, T1087.002 |
| `malware_execution.md` | Payload execution & LOLBins | T1059 |
| `sql_injection_dvwa.md` | SQL injection via DVWA | T1190 |

### Additional write-ups

| File | Topic |
|------|--------|
| `vulnerability_assessment.md` | Nmap-based vulnerability assessment across lab hosts |
| `reverse_shell_sim.md` | Reverse shell simulation notes |
| `malware_behavior_lab.md` | Malware behavior / telemetry lab notes |

---

## Goal

Produce realistic attack data to support detection engineering, log analysis, and incident response workflows.
