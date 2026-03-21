# Portfolio Showcase: SOC Documentation & Incident Response Playbooks

**Analyst:** Stacy Bostick
**Core Competencies:** Tier 1/2 SOC Operations, Playbook Development, Alert Triage, Escalation Matricies

---

## 📓 Project Overview: SOC Playbook Engineering

Developed comprehensive Security Operations Center (SOC) documentation aimed at standardizing alert triage, reducing Mean Time to Resolve (MTTR), and ensuring consistent escalation procedures. This portfolio piece demonstrates the ability to translate complex security events into repeatable, human-readable processes for critical infrastructure defense.

---

## 🚨 Sample Document: T1-to-T2 Escalation Matrix

The following is an excerpt from a custom escalation matrix designed to empower Tier 1 analysts to make rapid, decisive judgments on alert handling.

### Tier 1 Resolution Guidelines (Close/Monitor)

| Security Incident Scenario | Required Action | Ticket Status |
|----------------------------|-----------------|---------------|
| Single failed login, no discernible pattern | Document and monitor entity | **Close** |
| Known false positive (verified whitelist) | Annotate with rule tuning ID | **Close** |
| Authorized penetration test / vulnerability scan | Verify with Change Management | **Close** |
| User locked out (< 5 attempts, known entity) | Verify identity with HR/Service Desk | **Close** |

### Tier 2 Escalation Triggers (Escalate)

| Security Incident Scenario | Justification | Urgency Level |
|----------------------------|---------------|---------------|
| **Successful login immediately following Brute Force** | High probability of Credential Compromise | 🔴 **Immediate** |
| **Kerberoasting detected (RC4 TGS Requests)** | Critical Service Account Hash Stolen | 🔴 **Immediate** |
| **Encoded PowerShell Execution (Suspicious Parent)** | Possible Malware execution / C2 beacon | 🔴 **Immediate** |
| **Lateral Movement (Admin Shares, WMI, WinRM)** | Active Breach in progress | 🔴 **Immediate** |
| **Mass File Modifications (Known extensions)** | Ransomware execution indicators | 🔴 **Immediate** |
| **New Domain Admin account created** | Attacker Persistence mechanism | 🟡 **Within 15 min** |

---

## 📋 Standardized Escalation Workflow Design

Engineered a 4-step warm-handoff process to ensure context is never lost during severity escalations:

1. **Artifact Consolidation:** Mandating the collection of Source/Dest IPs, Alert Name, Affected Accounts, and raw SPL query results prior to escalation.
2. **Ticketing Standardization:** Enforcing naming conventions (e.g., SOC-XXX) and dynamic priority assignment based on business impact.
3. **Communication Protocol:** Defining SLA-driven communication methods (Slack/Teams for standard P3/P4; Paging platforms for P1/P2 active breaches).
4. **Warm Handoff:** Verbal briefing to Tier 2 analysts to accelerate situational awareness.

---
*Available for freelance technical security writing, SOC playbook creation, and incident response process development.*
