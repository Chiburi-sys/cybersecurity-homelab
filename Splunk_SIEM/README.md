# SIEM Deployment & Detection Engineering (Splunk)

This folder documents the installation, configuration, and use of Splunk Enterprise as a SIEM solution in the home lab. It includes log ingestion via Sysmon and the Universal Forwarder, as well as complex SPL (Search Processing Language) queries for threat hunting.

## Contents

- [**Laboratory Setup Guide**](../Lab_Setup_Manual/splunk_setup.md) — Installing Splunk Enterprise on Ubuntu
- [**Forwarder Configuration**](../Lab_Setup_Manual/splunk_forwarder_setup.md) — Configuring data ingestion from Windows
- [`sysmon_config.md`](sysmon_config.md) — Sysmon installation and XML configuration
- [`spl_queries.md`](spl_queries.md) — Splunk detection queries and threat hunting
- [`alert_configuration.md`](alert_configuration.md) — Configuring real-time alerts in Splunk
- [`../Screenshots/Splunk/`](../Screenshots/Splunk/) — Dashboards, alerts, and search screenshots

## Goal

Demonstrate dual-SIEM deployment, log ingestion, alert configuration, and detection engineering skills using both Splunk and Wazuh.
