# SIEM Deployment & Detection Engineering (Splunk)

This folder documents the installation, configuration, and use of Splunk Enterprise as a SIEM solution in the home lab. It includes log ingestion via Sysmon and the Universal Forwarder, as well as complex SPL (Search Processing Language) queries for threat hunting.

## Contents

- [`splunk_install_ubuntu.md`](splunk_install_ubuntu.md) — Installation steps on Ubuntu Server
- [`sysmon_config_windows.md`](sysmon_config_windows.md) — Sysmon setup and configuration
- [`splunk_forwarder_setup.md`](splunk_forwarder_setup.md) — Universal Forwarder configuration for Splunk
- [`spl_queries.md`](spl_queries.md) — Splunk detection queries
- [`alert_configuration.md`](alert_configuration.md) — Configuring real-time alerts in Splunk
- `screenshots/` — Dashboards, alerts, and search examples

## Goal

Demonstrate dual-SIEM deployment, log ingestion, alert configuration, and detection engineering skills using both Splunk and Wazuh.
