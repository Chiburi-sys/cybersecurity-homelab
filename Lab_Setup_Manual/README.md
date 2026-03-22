# Lab Setup Manual: Complete Deployment Guide

This folder contains the step-by-step instructions, network diagrams, and configuration files required to build the entire cybersecurity laboratory from scratch. 

> [!NOTE]
> This "Manual" is separated from the rest of the portfolio to keep the project folders focused strictly on **Security Results and Detection Engineering**.

---

## 🛠️ Module 1: Network & Infrastructure
Before any security tools can be deployed, the underlying network must be established and isolated.
- [**Network Diagram**](network_diagram_updated.md) — Visual topology of the 4-VM lab environment.
- [**IP Address Map**](vm_ip_map_updated.md) — Static IP assignments for all nodes (DC01, Splunk, Win11, Kali).

---

## 🏗️ Module 2: Active Directory DS
Setting up the identity management layer for the laboratory.
- [**AD DS Setup Guide**](ad_setup_guide.md) — Windows Server 2022 promotion, OU structure, and User creation.

---

## 🔍 Module 3: Splunk SIEM Deployment
Infrastructural setup for the network-wide log management system.
- [**Splunk Enterprise Setup**](splunk_setup.md) — Installing Splunk on Ubuntu Server 22.04 LTS.
- [**Universal Forwarder Setup**](splunk_forwarder_setup.md) — Configuring log streaming from Windows endpoints.

---

## 🛡️ Module 4: Wazuh SIEM/XDR (Docker)
Host-based detection and automated response setup.
- [**Wazuh Docker Deployment**](wazuh_setup.md) — Spinning up the Wazuh stack and registering agents.

---

## 🕸️ Module 5: Vulnerable Web App
Setting up a target for pentesting and detection practice.
- [**DVWA Setup Guide**](dvwa_setup_guide.md) — Installing and configuring the Damn Vulnerable Web App.

---

*Once the lab is built according to these guides, you can begin generating attacks and viewing the results in the project folders!*
