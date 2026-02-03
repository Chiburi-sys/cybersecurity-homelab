# Incident Report — [Insert Incident Title]
**Date:** YYYY-MM-DD  
**Analyst:** Stacy  
**Environment:** Home Lab (Ubuntu Server, Windows 11, Kali Linux, Splunk SIEM)

---

## 1. Executive Summary
Brief overview of the incident, its impact, and resolution.

*Example:*  
A brute-force SSH attack was simulated from Kali Linux targeting Ubuntu Server. Splunk detected repeated failed login attempts and triggered an alert.

---

## 2. Incident Details
- **Incident Type:** (e.g., Brute Force, Malware Execution, SQL Injection)  
- **Target System:**  
- **Source System:**  
- **MITRE ATT&CK Mapping:**  
  - Tactic:  
  - Technique:  

---

## 3. Timeline of Events

| Time (UTC) | Event |
|------------|-------|
| HH:MM      | Attack initiated |
| HH:MM      | Logs ingested by Splunk |
| HH:MM      | Alert triggered |
| HH:MM      | Investigation started |

---

## 4. Indicators of Compromise (IOCs)
- Source IP  
- Target IP  
- Usernames attempted  
- Malicious commands or payloads  
- File hashes (if applicable)

---

## 5. Log Analysis
Summarize relevant logs and queries used.

**Example SPL Query:**
```spl
index=auth sourcetype=linux_secure "Failed password"
| stats count by src, user
