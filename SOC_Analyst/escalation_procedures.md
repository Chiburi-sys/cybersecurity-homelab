# SOC Escalation Procedures

**Author:** Stacy Bostick  
**Role:** Tier 1 SOC Analyst  
**Environment:** cybersec.local

---

## Escalation Matrix

### When to Handle (Tier 1)

| Scenario | Action | Close? |
|----------|--------|--------|
| Single failed login, no pattern | Document and monitor | Yes |
| Known false positive (whitelisted) | Close with note | Yes |
| Authorized pen test / scan | Verify with change management, close | Yes |
| User forgot password (< 5 attempts) | Verify with service desk, close | Yes |
| Scheduled task triggering alert | Verify legitimacy, add tuning rule | Yes |
| DNS query to known benign domain | Whitelist, close | Yes |

### When to Escalate (Tier 2)

| Scenario | Why | Urgency |
|----------|-----|---------|
| Successful login after brute force | Credential compromised | 🔴 Immediate |
| Kerberoasting detected (RC4 TGS) | Service account hash stolen | 🔴 Immediate |
| Encoded PowerShell execution | Possible malware/C2 | 🔴 Immediate |
| Lateral movement detected | Active breach | 🔴 Immediate |
| Data exfiltration indicators | Active breach | 🔴 Immediate |
| Multiple hosts compromised | Widespread incident | 🟡 Within 15 min |
| Ransomware indicators | Critical threat | 🔴 Immediate |
| New admin account created | Persistence | 🟡 Within 15 min |

---

## Escalation Process

### Step 1: Document Before Escalating

Before contacting Tier 2, ensure you have:

- [ ] Alert name, time, and severity
- [ ] Source and destination IPs
- [ ] Affected account(s)
- [ ] SPL queries and results
- [ ] IOCs identified
- [ ] Your initial assessment

### Step 2: Create the Ticket

- Open a ticket in the ticketing system (SOC-XXX)
- Set priority based on impact and urgency
- Attach all investigation artifacts

### Step 3: Contact Tier 2

| Method | When |
|--------|------|
| Slack/Teams channel | Standard escalation |
| Phone/page | Active breach or ransomware |
| Email | Low-urgency follow-up |

### Step 4: Perform Warm Handoff

- Brief Tier 2 analyst verbally on findings
- Walk through your investigation steps
- Share the ticket ID and any dashboards
- Remain available for follow-up questions

---

## Priority Definitions

| Priority | Label | Response Time | Example |
|----------|-------|---------------|---------|
| P1 | Critical | Immediate | Active breach, ransomware, data exfil |
| P2 | High | < 30 minutes | Credential compromise, C2 detected |
| P3 | Medium | < 4 hours | Port scan, recon, single failed login |
| P4 | Low | < 24 hours | Policy violation, info gathering |

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad |
|---------|-------------|
| Closing a TP without investigation | Miss active compromise |
| Escalating every alert | Wastes T2 time, shows lack of judgment |
| Not documenting investigation | T2 repeats your work |
| Changing firewall rules without approval | Unauthorized changes |
| Ignoring correlated alerts | Miss the full attack chain |

---

*This escalation guide is part of a cybersecurity home lab portfolio demonstrating Tier 1 SOC Analyst skills.*
