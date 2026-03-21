# Wazuh SIEM & XDR Deployment

This folder documents the installation, configuration, and practical application of Wazuh as an open-source SIEM and XDR (Extended Detection and Response) solution in the home lab.

---

## 📁 Contents

| File | Purpose |
|------|---------|
| `wazuh_setup.md` | Step-by-step guide for Docker-based deployment of the Wazuh stack |
| `wazuh_detection_engineering.md` | Documentation of custom rule creation, decoder logic, and alerting |
| `wazuh_local_rules.xml` | The actual custom XML rules implemented on the Wazuh Manager |
| `wazuh_screenshot_guide.md` | Scenarios and triggers used to generate visual evidence for the portfolio |
| `vulnerability_assessment.md` | Analyzing agent-based vulnerability scan results and risk posture |
| `wazuh_soar_architecture.md` | Conceptual design for automated response and SOAR integration |

---

## 🚀 Key Capabilities Demonstrated

- **Endpoint Monitoring** — Deploying Wazuh agents to Windows and Linux hosts for real-time telemetry.
- **File Integrity Monitoring (FIM)** — Detecting unauthorized changes to critical system files and configurations.
- **Vulnerability Detection** — Continuous scanning for CVEs and outdated software on managed endpoints.
- **Custom Rule Development** — Writing tailored XML rules to detect specific attack patterns (e.g., brute force, suspicious shells).
- **Log Management & Visualization** — Using the Wazuh Dashboard (based on Kibana) to visualize security events and trends.

---

## 🎯 Goal

The goal of this section is to showcase a scalable, host-based detection pipeline that complements the network-focused logging of Splunk, providing a comprehensive "Defense in Depth" visibility across the lab.
