# Wazuh Rootkit & Anomaly Detection (Rootcheck)

**Report Date:** 2026-03-22  
**Prepared By:** Stacy (SOC Analyst)  
**Host Name:** `stacy-systemproductname` (Garuda Linux)  
**Detection Source:** Wazuh Rootcheck Module

---

## 1. Executive Summary

During a scheduled system scan using the **Wazuh Rootcheck** module, multiple critical security anomalies were detected on the host `stacy-systemproductname`. The SIEM flagged several core system binaries, including `/usr/sbin/passwd`, `/usr/bin/passwd`, and `/sbin/passwd`, as potentially **trojaned**. 

A "trojaned" binary is one that has been modified by an attacker (often part of a rootkit) to hide malicious activity, maintain persistence, or intercept sensitive data (like user passwords). Detecting these anomalies is a high-priority SOC event that requires immediate investigation and forensic analysis.

## 2. Evidence & Detection (Rule 510)

![Wazuh Rootcheck Trojaned Binaries Detection](/home/stacy/Cyber Security Portfolio/Screenshots/Wazuh/wazuh_rootkit_detection_passwd.png)

### 2.1. Rule Trigger: 510 - Host-based anomaly detection
- **Severity Rating:** Level 7 (Critical Anomaly)
- **Description:** Host-based anomaly detection event (rootcheck).
- **Findings:** The scan engine utilized a generic signature (`bash|file|.h|proc|.h/|dev/ttyo|/dev/|[-a_uvxz]`) to identify non-standard code or strings embedded within the `passwd` binary. This specific signature often indicates the presence of hidden backdoors or anti-forensic techniques.

### 2.2. Affected File List
The following binaries failed the integrity/anomaly check:
1. `/usr/sbin/passwd`
2. `/usr/bin/passwd`
3. `/sbin/passwd`
4. `/bin/passwd`

## 3. Threat Analysis & Business Risk

### 3.1. The Rootkit Vector (T1014)
The findings align with MITRE ATT&CK **T1014 (Rootkit)**. If an attacker replaces the standard `passwd` utility with a malicious version, they can:
- Intercept and log plaintext passwords whenever a user changes their credentials.
- Bypass authentication entirely using a hardcoded "master password".
- Hide other malicious processes from the system's process list.

### 3.2. Business Impact
A compromised `passwd` binary on a production machine represents a **complete compromise of the authentication chain**. Credential theft at this level allows for rapid lateral movement across the network and eventual domain dominance.

## 4. SOC Forensic Investigation & Resolution

As a SOC Analyst, it is critical not to rely solely on a single tool. Upon receiving the "Trojaned Binary" alert, I conducted a forensic investigation to rule out a false positive.

### 4.1. Verification via Package Manager (`pacman`)
On Arch-based systems like Garuda, the native package manager can verify the integrity of installed files against the official repository hashes.

![Pacman Integrity Check Proof](/home/stacy/Cyber Security Portfolio/Screenshots/Wazuh/wazuh_pacman_integrity_check.png)

```bash
sudo pacman -Qk shadow
```
**Result:** `shadow: 576 total files, 0 altered files, 0 missing files`

### 4.2. Timeline Analysis
- **Installation Date:** November 16, 2025
- **File Modification Date:** June 27, 2025
- **Conclusion:** The file has not been modified since the package was last installed/updated by the system.

### 4.3. Final Determination: False Positive (FP)
This alert is a confirmed False Positive. It was triggered by a generic Wazuh signature matching a legitimate segment of the `shadow` package binary as compiled for the Arch Linux architecture. No system compromise occurred.

## 5. Portfolio Insight: The Value of "False Positives"

Including False Positive investigations in a SOC portfolio demonstrates:
1. **Critical Thinking:** Not every alert is a breach. Analysts must know how to validate findings.
2. **OS Mastery:** Proficiency with native Linux utilities (`pacman`, `stat`, `grep`) to perform secondary verification.
3. **Efficiency:** Quickly triaging and clearing noise allows the SOC to focus on real, substantiated threats.

---

*This investigation demonstrates the full incident lifecycle: Detection, Forensic Analysis, and Resolution.*
