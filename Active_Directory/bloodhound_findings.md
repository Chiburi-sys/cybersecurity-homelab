# BloodHound AD Analysis — Future Work

**Status:** Planned  
**Environment:** VirtualBox Home Lab (cybersec.local)

---

## Overview

BloodHound is a graph-based Active Directory analysis tool that maps relationships between domain objects (users, groups, computers, GPOs) to identify attack paths. It uses the Neo4j graph database to visualize paths to Domain Admin and other high-value targets.

---

## Planned Scope

### Data Collection

```bash
bloodhound-python -u j.smith -p 'Password123!' -d cybersec.local -ns 192.168.50.5 -c All
```

### Analysis Goals

- Map shortest path to Domain Admin from `j.smith`
- Identify Kerberoastable accounts (should find `svc_sql`)
- Detect over-permissioned users or groups
- Visualize trust relationships within `cybersec.local`

### Expected Findings

| Finding | Expected Result |
|---------|----------------|
| Kerberoastable Users | `svc_sql` (SPN registered) |
| Domain Admins | `Administrator`, `s.admin` |
| Attack Paths | `j.smith` → Kerberoast `svc_sql` → potential escalation |

---

## Why This Is Planned (Not Yet Executed)

BloodHound requires:

- Neo4j database installation on Kali
- Sufficient domain activity to generate meaningful graph data
- Additional domain objects (GPOs, nested groups) for realistic attack paths

The current lab focuses on foundational AD attacks (Kerberoasting, password spraying). BloodHound analysis will be added as the lab matures with more complex group structures and delegation configurations.

---

*This document is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
