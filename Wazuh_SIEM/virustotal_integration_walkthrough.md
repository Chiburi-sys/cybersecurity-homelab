# Technical Report: Wazuh & VirusTotal Malware Detection Pipeline

**Author:** Stacy  
**Date:** 2026-04-05  
**Subject:** Real-Time Malware Ingestion & Response Integration  

---

## 🧭 Executive Summary
To enhance host-level security on the primary Arch Linux (Garuda) endpoint, I engineered a real-time malware detection pipeline. This system leverages Wazuh's File Integrity Monitoring (FIM) to capture new file arrivals, which are then automatically cross-referenced against the **VirusTotal API** (70+ Antivirus engines). Any positive detections are instantly broadcast to the SOC Discord channel via a custom Python integration.

## 🛠️ Implementation Architecture

### 1. Endpoint Monitoring (The "Watcher")
I configured the Wazuh Agent on the host PC to monitor the `Downloads` directory in real-time. This ensures that any file arriving via a web browser or external transfer triggers the detection chain immediately.

**Configuration (`ossec.conf`):**
```xml
<syscheck>
  <directories check_all="yes" realtime="yes">/home/stacy/Downloads</directories>
</syscheck>
```

### 2. SIEM API Orchestration (The "Evaluator")
The Wazuh Manager was configured with a dedicated integration block using a VirusTotal API key. This component listens for FIM events (Rule 554 - File Added) and performs an asynchronous hash lookup.

**Configuration (`ossec.conf`):**
```xml
<integration>
  <name>virustotal</name>
  <api_key>[REDACTED]</api_key>
  <rule_id>554,550</rule_id>
  <alert_format>json</alert_format>
</integration>
```

---

## 🚧 Challenging Pitfalls & SOC Troubleshooting

During this integration, I encountered and resolved two critical "real-world" security engineering obstacles:

### ⚠️ Issue A: Discord API Cloudflare Block (403 Forbidden)
**Symptom:** Wazuh was successfully detecting malware internally, but the Discord Webhook was returning `403 Access Denied` / `Error 1010`.  
**Root Cause:** Discord's Cloudflare protection blocks "headless" Python `urllib` requests that do not provide a modern browser `User-Agent` header.  
**Resolution:** I refactored the `custom-discord.py` integration script to include a spoofed Chrome `User-Agent` header, circumventing the block and allowing the SIEM to communicate with the SOC channel.

### ⚠️ Issue B: Wazuh Integration Security Policy (Permissions)
**Symptom:** The `wazuh-integratord` daemon refused to execute the integration script.  
**Root Cause:** Wazuh follows strict **Security Through Integrity** principles. If a script has "Write" permissions enabled for non-root users, the engine disables it to prevent "Integration Hijacking".  
**Resolution:** I applied a strict `chmod 750` and `chown root:wazuh` policy to the script deep inside the Docker container, satisfying the SIEM's zero-trust requirement.

---

## 🧪 Validation & Testing

To verify the end-to-end functionality, I executed a **Red Team Simulation** by dropping a harmless `EICAR` anti-malware test string into the monitored directory.

**Detection Workflow:**
1. **User Action:** `echo 'EICAR-STRING' > ~/Downloads/eicar.com`
2. **FIM Event:** Wazuh Agent detects the new file and sends the SHA256 hash to the Manager.
3. **API Lookup:** Manager queries VirusTotal; 61+ AV engines flag the file as malicious.
4. **Discord Alert:** The custom integration fires, delivering a high-severity alert to the SOC team.

![VirusTotal Detection in Discord](../Screenshots/Wazuh/wazuh_virustotal_eicar_detection.png)

## 📈 Conclusion
This integration significantly reduces the "Identification Time" for malware downloads from minutes/hours to **under 10 seconds**. The host is now actively protected by a global intelligence network, providing the SOC with immediate, actionable data on every file dropped onto the system.
