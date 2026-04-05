# SQL Injection — DVWA — Future Work

**Status:** Planned  
**MITRE ATT&CK:** T1190 — Exploit Public-Facing Application

---

## Planned Scope

Perform SQL injection attacks against DVWA (Damn Vulnerable Web Application) at varying security levels to demonstrate web application penetration testing skills.

### Attack Scenarios

| Level | Technique | Goal |
|-------|-----------|------|
| Low | Basic `' OR 1=1 --` | Extract all users |
| Medium | Numeric injection | Bypass input filtering |
| High | Blind SQL injection | Enumerate via boolean responses |

### Tools

- **Burp Suite** — Intercept and modify HTTP requests
- **sqlmap** — Automated SQL injection testing
- **Browser DevTools** — Manual parameter manipulation

### Detection

```spl
index=main sourcetype=access_combined
| regex _raw="(?i)(union|select|from|where|drop|insert|update|delete|--|;)"
| table _time, clientip, uri_path, status
```

---

*This document is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
