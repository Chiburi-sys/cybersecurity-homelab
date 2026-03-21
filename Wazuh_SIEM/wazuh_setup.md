# Wazuh SIEM Setup — Deployment & Post-Installation Guide

**Date:** 2026-03-17  
**Analyst:** Stacy  
**Environment:** Garuda Linux (Arch-based, bare metal)  
**Wazuh Version:** 4.14.3 (Docker) / 4.14.4 (Agent)
---

## Overview

This document covers the complete deployment and hardening of Wazuh SIEM on a personal Garuda Linux workstation. The server stack (Manager, Indexer, Dashboard) runs via Docker Compose, while the Wazuh agent runs natively as a systemd service to monitor the host. This provides real-time endpoint security monitoring including intrusion detection, file integrity monitoring, rootkit detection, vulnerability scanning, and CIS benchmark assessment.

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│                 Garuda Linux Host                 │
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │           Docker Compose Stack              │  │
│  │                                             │  │
│  │  ┌───────────────┐  ┌───────────────────┐   │  │
│  │  │ wazuh.manager │  │  wazuh.indexer    │   │  │
│  │  │  :1514 (TCP)  │  │  :9200 (HTTPS)   │   │  │
│  │  │  :1515 (TCP)  │  │  (OpenSearch)     │   │  │
│  │  │  :514  (UDP)  │  └───────────────────┘   │  │
│  │  │  :55000(API)  │                          │  │
│  │  └───────┬───────┘  ┌───────────────────┐   │  │
│  │          │          │ wazuh.dashboard   │   │  │
│  │          │          │  :443 (HTTPS)     │   │  │
│  │          │          │  (Web UI)         │   │  │
│  │          │          └───────────────────┘   │  │
│  └──────────┼──────────────────────────────────┘  │
│             │                                      │
│  ┌──────────┴──────────┐                          │
│  │   wazuh-agent       │                          │
│  │   (native systemd)  │                          │
│  │   → 127.0.0.1:1514  │                          │
│  └─────────────────────┘                          │
└──────────────────────────────────────────────────┘
```

---

## System Requirements (Met)

| Resource | Available | Required |
|----------|-----------|----------|
| CPU | Ryzen 7 7800X3D (16 threads) | 4 cores min |
| RAM | 30 GB | 4-8 GB |
| Disk | 212 GB free | ~10-20 GB |
| Docker | v29.3.0 | ✅ |
| Docker Compose | v5.1.0 | ✅ |

---

## 1. Pre-Installation: Kernel Tuning

The Wazuh Indexer (OpenSearch) requires a high memory-mapped file limit.

```bash
# Permanent — persists across reboots
echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/99-wazuh.conf
sudo sysctl --system

# Verify
sysctl vm.max_map_count
# Expected: vm.max_map_count = 262144
```

**Why:** OpenSearch creates many memory-mapped areas for its Lucene indexes. The default Linux value (65530) causes `OutOfMemoryError` even with abundant RAM.

---

## 2. Docker Stack Deployment

```bash
# Clone official repo (specific stable version)
cd ~
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.3
cd wazuh-docker/single-node

# Generate SSL certificates for inter-component communication
docker compose -f generate-indexer-certs.yml run --rm generator

# Start the stack (detached)
docker compose up -d
```

### Verify All Containers Are Running

```bash
docker compose ps
```

**Expected:** All 3 containers show `Up` status:

| Container | Image | Ports |
|-----------|-------|-------|
| wazuh.manager | wazuh/wazuh-manager:4.14.3 | 1514, 1515, 514/udp, 55000 |
| wazuh.indexer | wazuh/wazuh-indexer:4.14.3 | 9200 |
| wazuh.dashboard | wazuh/wazuh-dashboard:4.14.3 | 443→5601 |

![Wazuh Docker Deployment Status](file:///home/stacy/Cyber Security Portfolio/Screenshots/Wazuh/Wazuh_docker_deployment.png)

---

## 3. Agent Installation (Garuda/Arch Linux)

```bash
# Install from AUR
yay -S wazuh-agent

# Configure agent to connect to manager on localhost
# Edit /var/ossec/etc/ossec.conf — set manager address:
#   <server><address>127.0.0.1</address></server>

# Enable and start the agent service
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

# Verify
systemctl status wazuh-agent
```

**Expected:** Service shows `active (running)` with these daemons:

- `wazuh-agentd` — Communication with manager
- `wazuh-execd` — Active response execution
- `wazuh-syscheckd` — File integrity monitoring
- `wazuh-logcollector` — Log ingestion
- `wazuh-modulesd` — Vulnerability detection, SCA, etc.

---

## 4. Auto-Start on Boot (Already Configured)

Three layers ensure Wazuh starts automatically when you power on:

### Layer 1: Docker Service

```bash
systemctl is-enabled docker
# Output: enabled
```

Docker starts automatically on boot via systemd.

### Layer 2: Container Restart Policy

All three containers in `docker-compose.yml` have:

```yaml
restart: always
```

This means Docker automatically restarts the Wazuh containers whenever the Docker daemon starts (i.e., on boot) or if a container crashes.

### Layer 3: Wazuh Agent Service

```bash
systemctl is-enabled wazuh-agent
# Output: enabled
```

The native agent starts automatically on boot via systemd.

### Boot Sequence

```
Power On → systemd starts → Docker daemon starts
                           → wazuh-agent.service starts
                           ↓
                     Docker restarts containers (restart: always)
                           ↓
                     wazuh.indexer comes up (:9200)
                     wazuh.manager comes up (:1514)
                     wazuh.dashboard comes up (:443)
                           ↓
                     Agent connects to Manager (127.0.0.1:1514)
                           ↓
                     Monitoring active ✅
```

**No action needed.** Everything is already configured to start on boot.

---

## 5. Post-Installation Checklist

### ✅ Immediate (Do Now)

| # | Task | How | Status |
|---|------|-----|--------|
| 1 | **Access Dashboard** | Open `https://localhost` in browser | ✅ Done |
| 2 | **Login** | `admin` / `SecretPassword` | ✅ Done |
| 3 | **Verify Agent** | Dashboard → Agents → Confirm "stacy-systemproductname" shows Active (green) | ✅ Done |
| 4 | **Check Alerts** | Dashboard → Security Events → Confirm events flowing (191 captured) | ✅ Done |

![Wazuh Dashboard with Active Agent](file:///home/stacy/Cyber Security Portfolio/Screenshots/Wazuh/Wazuh_dashboard_active_agent.png)

### 5. Change Default Password
| 6 | **Enable Dark Mode** | Dashboard → ☰ Menu → Management → Dashboard Settings → Appearance → Dark Mode | ⬜ Pending |

### 🔧 Hardening (Do This Week)

| # | Task | Why |
|---|------|-----|
| 7 | **Configure FIM** | Monitor `/etc`, `/bin`, `/usr/bin`, `/home/stacy/.ssh` for unauthorized changes |
| 8 | **Review SCA Results** | Dashboard → Configuration Assessment → See CIS benchmark failures |
| 9 | **Check Vulnerabilities** | Dashboard → Vulnerability Detection → Review CVEs in installed packages |
| 10 | **Set Up Active Response** | Auto-block IPs after repeated SSH failures |

### 📋 Ongoing (Weekly Routine)

| # | Task | Why |
|---|------|-----|
| 11 | **Review Security Events** | Dashboard → Security Events → Filter by severity (Medium/High) |
| 12 | **Check MITRE ATT&CK** | Dashboard → MITRE ATT&CK → See techniques detected on your host |
| 13 | **Review FIM Changes** | Dashboard → File Integrity Monitoring → Check for unexpected file modifications |
| 14 | **Update Wazuh** | `cd ~/wazuh-docker/single-node && docker compose pull && docker compose up -d` |

---

## 6. Changing the Default Admin Password

This is a multi-step process because the password is used by three components.

### Step 1: Generate Password Hash

```bash
# Run the hash tool inside the indexer container
docker exec -it single-node-wazuh.indexer-1 bash -c \
  "export JAVA_HOME=/usr/share/wazuh-indexer/jdk && \
   /usr/share/wazuh-indexer/plugins/opensearch-security/tools/hash.sh"
```

Enter your new password when prompted. Copy the bcrypt hash output.

### Step 2: Update internal_users.yml

Edit `~/wazuh-docker/single-node/config/wazuh_indexer/internal_users.yml`:

```yaml
admin:
  hash: "<paste-your-new-hash-here>"
  reserved: true
  backend_roles:
    - "admin"
```

### Step 3: Update docker-compose.yml

Edit `~/wazuh-docker/single-node/docker-compose.yml` — replace `SecretPassword` with your new password in:

- `wazuh.manager` → `INDEXER_PASSWORD`
- `wazuh.dashboard` → `INDEXER_PASSWORD`

### Step 4: Restart and Apply

```bash
cd ~/wazuh-docker/single-node

# Restart the stack
docker compose down
docker compose up -d

# Apply the security config inside the indexer
docker exec -it single-node-wazuh.indexer-1 bash -c \
  "export JAVA_HOME=/usr/share/wazuh-indexer/jdk && \
   bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/securityadmin.sh \
   -cd /usr/share/wazuh-indexer/config/opensearch-security/ \
   -nhnv \
   -cacert /usr/share/wazuh-indexer/config/certs/root-ca.pem \
   -cert /usr/share/wazuh-indexer/config/certs/admin.pem \
   -key /usr/share/wazuh-indexer/config/certs/admin-key.pem \
   -icl \
   -h localhost"
```

### Step 5: Verify

```bash
# Test new credentials
curl -sk -u admin:YOUR_NEW_PASSWORD https://localhost:9200 | head -5
```

---

## 7. Useful Commands Reference

### Stack Management

```bash
# Check container status
cd ~/wazuh-docker/single-node && docker compose ps

# View manager logs (real-time)
docker compose logs -f wazuh.manager

# Restart entire stack
docker compose restart

# Stop stack (frees ~3-5 GB RAM for gaming, etc.)
docker compose down

# Start stack back up
docker compose up -d
```

### Agent Management

```bash
# Check agent status
systemctl status wazuh-agent

# Restart agent (after config changes)
sudo systemctl restart wazuh-agent

# View agent logs
sudo tail -f /var/ossec/logs/ossec.log
```

### API Access

```bash
# Get auth token from Wazuh API
TOKEN=$(curl -sk -u wazuh-wui:MyS3cr37P450r.*- -X POST \
  https://localhost:55000/security/user/authenticate | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

# List agents
curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:55000/agents?pretty

# Get agent summary
curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:55000/overview/agents?pretty
```

---

## 8. What Each Dashboard Module Does

### Endpoint Security

| Module | What It Does |
|--------|-------------|
| **Configuration Assessment** | Scans your system against CIS benchmarks and security best practices |
| **Malware Detection** | Checks for indicators of compromise from malware infections |
| **File Integrity Monitoring** | Alerts when files in monitored directories change unexpectedly |

### Threat Intelligence

| Module | What It Does |
|--------|-------------|
| **Threat Hunting** | Search and filter through all security events for investigation |
| **Vulnerability Detection** | Cross-references your installed packages against CVE databases |
| **MITRE ATT&CK** | Maps detected events to adversary tactics and techniques |

### Security Operations

| Module | What It Does |
|--------|-------------|
| **IT Hygiene** | System inventory — installed packages, open ports, running processes |
| **Docker** | Monitors Docker container events (creation, start, stop, pause) |

---

## Key Takeaways

1. **Wazuh auto-starts with your PC** — Docker service, container restart policies, and the agent systemd service ensure full monitoring from boot.
2. **Stop the stack when gaming** — `docker compose down` frees ~3-5 GB RAM. Start it back with `docker compose up -d`.
3. **Check your dashboard weekly** — Review Security Events, FIM changes, and Vulnerability Detection.
4. **Change the default password first** — `SecretPassword` is publicly known. See Section 6.
5. **Optimize for SOC Workflow** — Edit `/usr/share/wazuh-dashboard/config/opensearch_dashboards.yml` to set `opensearch_security.session.ttl: 43200000` (12 hours) to avoid constant timeouts, and `uiSettings.overrides.theme:darkMode: true` to enforce a dark UI globally.
6. **Deploy SOAR Integrations** — As detailed in `wazuh_soar_architecture.md`, deploy the Python Discord integration in the manager container and configure Active Response to automatically drop attackers' IPs if brute-force thresholds are met.
7. **This complements your Splunk lab** — Splunk monitors your Windows VMs, Wazuh monitors your real host. Two SIEMs on one resume.

---
*This setup guide is maintained as part of a cybersecurity portfolio. Wazuh deployment running on Garuda Linux (bare metal) with Docker.*
