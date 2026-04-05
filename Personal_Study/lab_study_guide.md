# 🛡️ Lab Study Guide: "Under the Hood" Summary

This document is your "cheat sheet" for the technical background of your home lab. It explains the complex parts that happened behind the scenes so you can speak confidently to a hiring manager.

---

## 🌐 1. Network & Infrastructure

### **The Setup:**
- **Host OS:** Garuda Linux (Arch-based).  
- **Virtualization:** VirtualBox with a custom **Internal Network (LabNet)**.  
- **Gateway:** All VMs share a private 192.168.50.0/24 subnet.

### **Talking Points:**
- *"I chose an Internal Network setup to isolate the lab from my home Wi-Fi—this prevents any simulation traffic from leaking onto my real devices."*
- *"I used static IPs for every VM (DC01, Ubuntu, Windows 11) to ensure the SIEM links don't break between restarts."*

---

## 📊 2. The SIEM Pipeline: Splunk

### **The Setup:**
- **Server:** Splunk Enterprise running on **Ubuntu Server**.  
- **Troubleshooting:** The "Splunk 10.2 OpenSSL" issue.  

### **Talking Points:**
- *"One major hurdle was a version conflict between Splunk 10.2 and Ubuntu's OpenSSL. I had to manually generate my own Certificate Authority (CA) and server/private keys using CLI `openssl` commands and move them into the `auth` directory. It’s a great example of troubleshooting vendor software bugs in a Linux environment."*

---

## 🐕 3. The SIEM/EDR Layer: Wazuh

### **The Setup:**
- **Manager:** Wazuh Indexer and Manager running in **Docker Containers**.  
- **Automation:** SOAR-style automated alerts sent via **Webhook** to **Discord**.  

### **Talking Points:**
- *"I deployed Wazuh via Docker on my host machine—this gives me visibility into my host OS (Garuda) while keeping the lab isolated. I integrated it with Discord, so if a high-severity alert fires (like a root login or common attack vector), I get an instant notification on my phone."*

---

## 📁 4. Active Directory & Endpoint Hardening

### **The Setup:**
- **DC01:** Windows Server 2022 Domain Controller.  
- **Logging:** **Sysmon (System Monitor)** installed on all Windows endpoints.  

### **Talking Points:**
- *"I didn't stop at native Windows logs. I installed Sysmon with a custom configuration to get visibility into process creation (EventCode 1) and network connections. Without Sysmon, sophisticated attacks like base64-encoded PowerShell scripts would be much harder to detect in Splunk."*

---

## ⚔️ 5. Attack & Detection Logic

### **The Setup:**
- **Attackers:** Kali Linux (Nmap, CrackMapExec, Impacket).  
- **Detections:** Custom **SPL (Search Processing Language)** queries and **Wazuh XML rules**.  

### **Talking Points:**
- *"When I simulate a Kerberoasting attack, I look for EventCode 4769 in Splunk. I specifically target RC4 encryption downgrades, which is a classic indicator that an attacker is harvesting service tickets for offline cracking."*
- *"For Brute Force vs. Password Spray: I built alerts that distinguish the two. One account being hit 50 times? Brute Force. Fifty accounts being hit once? Password Spray. This allows for more targeted incident response."*

---

## 🚦 Summary Key Phrases

- *"I treat my lab like a production pipeline."*
- *"If it isn't documented, it never happened."*
- *"My philosophy is 'Learn how to break it so you know how to build it stronger'."*

---

*Study this guide along with your `interview_prep.md` to be 100% ready for your interview!*
