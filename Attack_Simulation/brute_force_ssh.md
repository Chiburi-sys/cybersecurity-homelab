# SSH Brute Force Attack Simulation

**Date:** 2026-02-28  
**Analyst:** Stacy Bostick  
**MITRE ATT&CK:** T1110.001 — Brute Force: Password Guessing  
**Environment:** VirtualBox Home Lab

---

## 🎯 Objective

- Simulate a real-world brute-force attack against SSH
- Generate authentication logs for Splunk ingestion
- Validate detection rules for repeated failed logins
- Observe syslog behavior and Splunk correlation

---

## 🧠 Environment

- **Attacker:** Kali Linux (192.168.50.30)  
- **Target:** Ubuntu Server (192.168.50.10)  
- **Service:** SSH (port 22)  
- **Tool:** Hydra

---

## 🛠️ Attack Execution

### Hydra Command

```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.50.10
```

### Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `-l root` | Username | Target the root account |
| `-P rockyou.txt` | Password list | Common password wordlist |
| `ssh://192.168.50.10` | Target | SSH service on Ubuntu Server |

---

## Expected Output

```
Hydra v9.5 (c) 2023 by van Hauser/THC
[DATA] max 16 tasks per 1 server, overall 16 tasks
[DATA] attacking ssh://192.168.50.10:22/
[STATUS] 64.00 tries/min, 64 tries in 00:01h
```

Each failed attempt generates a log entry in `/var/log/auth.log`:

```
sshd[12345]: Failed password for root from 192.168.50.30 port 54321 ssh2
```

---

## Splunk Detection

### Query — Failed SSH Logins

```spl
index=main sourcetype=syslog "Failed password"
| stats count by src_ip, user
| where count > 5
| sort -count
```

### Query — SSH Login Timeline

```spl
index=main sourcetype=syslog ("Failed password" OR "Accepted password") src_ip="192.168.50.30"
| timechart span=1m count by action
```

---

## Prevention & Hardening

| Control | Implementation |
|---------|---------------|
| Rate limiting | Install `fail2ban` — ban after 3 failures for 10 min |
| Key-based auth | Disable password auth in `/etc/ssh/sshd_config` |
| Root login | Set `PermitRootLogin no` in sshd_config |
| Port change | Move SSH to a non-standard port |
| Firewall | Use UFW to restrict SSH to known IPs |

### fail2ban Configuration

```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
maxretry = 3
bantime = 600
findtime = 600
```

---

## Key Takeaways

- Hydra can attempt hundreds of passwords per minute against SSH
- Without fail2ban, there is no rate limiting on SSH login attempts
- Splunk can ingest syslog from Ubuntu to detect brute force patterns
- Defense-in-depth (key auth + fail2ban + firewall) is essential

---

*This attack simulation is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
