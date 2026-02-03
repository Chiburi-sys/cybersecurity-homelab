# SSH Brute Force Attack Simulation

This document details a simulated SSH brute-force attack performed from Kali Linux against the Ubuntu Server host. The purpose of this simulation is to generate authentication telemetry for Splunk SIEM and practice detection engineering.

---

## 🎯 Objective

- Simulate a real-world brute-force attack  
- Generate authentication logs for Splunk  
- Validate detection rules for repeated failed logins  
- Observe Syslog and Splunk ingestion behavior  

---

## 🧠 Environment

- **Attacker:** Kali Linux (192.168.50.30)  
- **Target:** Ubuntu Server (192.168.50.10)  
- **Service:** SSH (port 22)  
- **Tool:** Hydra  

---

## 🛠️ Attack Execution

### Hydra Command Used

```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.50.10
