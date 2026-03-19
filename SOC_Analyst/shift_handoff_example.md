# Shift Handoff Report

**Date:** 2026-03-02  
**Analyst:** Stacy Bostick  
**Shift:** Day (08:00 – 20:00 EST)  
**Handing Off To:** Night Shift Analyst

---

## Shift Summary

Busy shift with an active attack chain detected and investigated. A password spray from 192.168.50.30 led to credential compromise of `j.smith`, which was then used for Kerberoasting against the `svc_sql` service account. Two tickets escalated to Tier 2.

---

## Open Incidents (Requires Attention)

| Ticket | Alert | Status | Priority | Notes |
|--------|-------|--------|----------|-------|
| SOC-001 | Brute force → j.smith compromised | Escalated to T2 | P2 | Awaiting password reset confirmation |
| SOC-002 | Kerberoasting on svc_sql | Escalated to T2 | P1 | T2 investigating if hash was cracked |

> ⚠️ **SOC-001 and SOC-002 are linked** — same attacker, same session. Monitor for any new activity from 192.168.50.30 or the j.smith account.

---

## Closed Tickets This Shift

| Ticket | Alert | Verdict | Resolution |
|--------|-------|---------|------------|
| SOC-003 | Port scan from Kali | TP (authorized) | Verified with change management |
| SOC-004 | PowerShell on Win11 | False Positive | Sysmon update script; tuning rule submitted |
| SOC-005 | AD password spray | TP | Documented, containment recommended |

---

## Alert Metrics

| Metric | Count |
|--------|-------|
| Total Alerts Reviewed | 10 |
| True Positives | 5 |
| False Positives | 3 |
| Benign | 2 |
| Tickets Created | 5 |
| Tickets Escalated | 2 |
| Tickets Closed | 3 |
| Tuning Recommendations | 2 |

---

## Things to Watch

1. **192.168.50.30** — Active attacker IP. If new connections appear from this IP, escalate immediately
2. **j.smith account** — Compromised. If any 4624 events appear before password reset is confirmed, isolate the target host
3. **svc_sql account** — Kerberoasting target. If any 4624 logins appear for this service account from unexpected sources, escalate as P1

---

## SIEM Health

| Component | Status |
|-----------|--------|
| Splunk Enterprise (192.168.50.10) | ✅ Healthy |
| Win11 Forwarder | ✅ Logs flowing |
| DC01 Forwarder | ✅ Logs flowing |
| Dashboard | ✅ All panels loading |
| Alerts | ✅ 4 alerts active, 0 disabled |

---

## Notes for Next Shift

- Tuning recommendation for SOC-004 (PowerShell FP) has been submitted but not yet applied. If the same alert fires again for `sysmon_update.ps1`, close as FP
- The alert triage log for today is complete at `SOC_Analyst/alert_triage_log.md`
- All investigation queries are documented in the tickets for reproducibility

---

*This shift handoff is part of a cybersecurity home lab portfolio demonstrating Tier 1 SOC Analyst skills.*
