# SOC Playbook — Brute Force Attack Response

**Playbook ID:** PB-001  
**Author:** Stacy Bostick  
**Last Updated:** 2026-03-01  
**Severity:** High  
**MITRE ATT&CK:** T1110 — Brute Force

---

## 1. Detection

### Trigger Conditions

- Splunk alert: `Brute Force — Multiple Failed Logins` fires
- More than 5 failed logins (EventCode 4625) from a single source IP

### Detection Query

```spl
index=main EventCode=4625
| stats count by src_ip, Account_Name
| where count > 5
| sort -count
```

---

## 2. Triage (First 5 Minutes)

### Step 1: Validate the Alert

- [ ] Open the triggered alert in Splunk
- [ ] Confirm the source IP and target account
- [ ] Check if this is a known false positive (service account, scheduled task)

### Step 2: Determine Scope

```spl
index=main EventCode=4625 src_ip="<ATTACKER_IP>"
| stats count by Account_Name, Failure_Reason
| sort -count
```

- [ ] How many accounts are being targeted?
- [ ] Is it one account (targeted) or many accounts (spray)?
- [ ] What is the failure reason?

### Step 3: Check for Success

```spl
index=main EventCode=4624 src_ip="<ATTACKER_IP>"
| table _time, Account_Name, LogonType, Workstation_Name
```

- [ ] Did any logins succeed from this IP?
- [ ] If YES → **Escalate immediately** to Incident Response

---

## 3. Investigation (Next 15 Minutes)

### Step 4: Profile the Source IP

- [ ] Is the IP internal or external?
- [ ] Run a WHOIS/reputation check on external IPs
- [ ] Check if this IP has been seen before in logs

```spl
index=main "192.168.50.30"
| stats count by source, EventCode
| sort -count
```

### Step 5: Check for Lateral Movement

```spl
index=main EventCode=4624 Account_Name="<COMPROMISED_ACCOUNT>"
| stats count by Workstation_Name, LogonType
```

- [ ] Has the targeted account logged into other systems?
- [ ] Any unusual logon types (Type 3 = Network, Type 10 = RDP)?

### Step 6: Review Timeline

```spl
index=main (EventCode=4625 OR EventCode=4624) src_ip="<ATTACKER_IP>"
| table _time, EventCode, Account_Name, Failure_Reason
| sort _time
```

---

## 4. Containment

### If Attack is Ongoing

- [ ] Block the source IP at the firewall
- [ ] Disable the targeted account(s) temporarily
- [ ] Force password reset for any successfully compromised accounts

### If Attack is From Internal Network

- [ ] Identify the compromised host
- [ ] Isolate the host from the network
- [ ] Begin endpoint forensics

---

## 5. Remediation

- [ ] Reset passwords for all targeted accounts
- [ ] Enable account lockout policy (lock after 5 failed attempts)
- [ ] Review and strengthen password policy
- [ ] Add source IP to blocklist
- [ ] Enable MFA for all admin accounts

---

## 6. Documentation

- [ ] Complete incident report using template
- [ ] Record IOCs (IPs, usernames, timestamps)
- [ ] Update detection rules if necessary
- [ ] Add to lessons learned

---

## 7. False Positive Checklist

| Scenario | Action |
|---|---|
| Service account with wrong password in config | Fix config, whitelist account |
| User forgot password | Verify with user, close alert |
| Scheduled task with expired credentials | Update credentials, whitelist |
| VPN reconnection failures | Whitelist VPN gateway IP |
