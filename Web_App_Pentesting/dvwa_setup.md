# DVWA Setup — Future Work

**Status:** Planned  
**Application:** Damn Vulnerable Web Application (DVWA)

---

## Planned Setup

DVWA will be deployed on the Ubuntu Server (192.168.50.10) alongside Splunk to enable web application attack simulations with real-time log correlation.

### Installation Plan

1. Install Apache, PHP, and MariaDB on Ubuntu Server
2. Clone DVWA from GitHub
3. Configure database connection
4. Set security levels (Low → Medium → High)
5. Configure Apache access logs to forward to Splunk

### Architecture

```
Kali Linux (192.168.50.30) → HTTP → Ubuntu Server (192.168.50.10)
                                        ├── DVWA (port 80)
                                        └── Splunk (port 8000)
```

### Attacks to Execute

- SQL Injection (see `Attack_Simulation/sql_injection_dvwa.md`)
- Cross-Site Scripting (XSS) — Reflected and Stored
- Command Injection
- File Upload bypass
- CSRF token manipulation

---

*This document is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
