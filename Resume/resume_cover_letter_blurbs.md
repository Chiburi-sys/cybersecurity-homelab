# 📜 Resume & Cover Letter Lab Summary

This document provides ready-to-use blurbs and bullet points for your resume and cover letter. These are designed to highlight your technical proficiency, problem-solving skills, and hands-on experience.

---

## 📄 For Your Resume (Experience Section)

**Cybersecurity Detection & Incident Response Lab (Personal Project)**  
*Self-Built Virtualized SOC Environment*

- **Integrated Multi-Vendor SIEM Architecture:** Engineered a dual-SIEM pipeline using **Splunk Enterprise** and **Wazuh** to monitor a Microsoft Active Directory environment (Windows Server 2022/Windows 11).
- **Custom Detection Engineering:** Developed and tuned high-fidelity detection logic (SPL & XML) for MITRE ATT&CK techniques, including **Kerberoasting (T1558.003)** and **Password Spraying (T1110.003)**.
- **SOAR & Automation:** Implemented automated response playbooks using **Wazuh Active Response**, integrating Discord Webhooks for real-time SOC alerting and notification.
- **Endpoint Hardening & Visibility:** Deployed and configured **Sysmon** across Windows endpoints with custom XML filters to enhance process-level visibility and catch base64-encoded PowerShell scripts.
- **Technical Troubleshooting:** Resolved architectural deployment issues, including a high-level **OpenSSL/Splunk 10.2 conflict**, by manually managing Root CA certificates and private keys via Linux CLI.

---

## ✉️ For Your Cover Letter (Narrative)

### Option 1: The "Self-Starter" Narrative (Best for Apprenticeships)

"I believe that the best way to understand an attack is to defend against it. To bridge the gap between theory and practice, I built a production-grade cybersecurity home lab using Garuda Linux, Docker, and VirtualBox. This wasn't just a basic install; I engineered a full detection pipeline where I simulated Active Directory attacks like SMB brute-forcing and Kerberoasting, and then built the custom correlation rules in Splunk to catch them. This project taught me the 'under-the-hood' mechanics of security tools, from troubleshooting vendor software bugs to automating incident response via Discord."

### Option 2: The "Technical Deep Dive" Narrative (Best for SOC Analyst roles)

"My hands-on experience in my home lab has given me a deep appreciation for the 'Documentation-Detection-Defense' cycle. By deploying both Splunk and Wazuh, I’ve learned how to correlate disparate data sources into a single pane of glass. I take pride in 'Detection Engineering'—writing my own XML rules for Wazuh and SPL queries for Splunk to reduce false positives in a lab environment. Whether it's managing static IP topologies for a 4-VM internal network or hardening Windows Server 2022 GPOs, I thrive on the technical challenges that come with building and defending complex infrastructures."

---

## 💡 Quick "Impact" Stats for Interviews

- **Architecture:** 4-VM Isolated Internal Network + Docker Stack.
- **Log Sources:** Windows Security Event Logs, Sysmon, Linux Auth Logs, Wazuh FIM.
- **Threat Focus:** Identity-based attacks (AD), Network Recon, Persistence.
- **Automation:** Zero-latency alerting via Discord webhooks.

---

*Tip: When you copy these, make sure to adjust the tone to match your own voice!*
