# Incident Report: Unauthorized Modification of SSH Configuration

**Incident ID:** INC-2026-002  
**Date Reported:** 2026-03-22  
**Analyst:** Stacy  
**Detection Source:** Wazuh SIEM (File Integrity Monitoring)  
**Severity:** High  
**Status:** Closed

---

## 1. Executive Summary
At 02:15 UTC, the Wazuh SIEM triggered a Level 7 alert indicating that the SSH daemon configuration file (`/etc/ssh/sshd_config`) was modified on the endpoint `stacy-systemproductname`. An investigation revealed an unauthorized append command was executed by the `root` user, attempting to alter SSH persistence mechanisms. The modification was reverted, and the incident was closed with no lateral movement detected.

## 2. Event Timeline (UTC)
- **02:14:30** - Successful `su - root` escalation by local user.
- **02:15:02** - Wazuh File Integrity Monitoring (FIM) detects a checksum change on `/etc/ssh/sshd_config`.
- **02:15:05** - Wazuh generates Alert ID `550`: "Integrity checksum changed."
- **02:20:00** - SOC Analyst (Stacy) acknowledges the alert and begins investigation.
- **02:45:00** - File modification is analyzed, deemed malicious/unauthorized, and reverted to the known-good baseline.
- **03:00:00** - Incident closed.

## 3. Technical Details

### SIEM Detection Data (Wazuh)
- **Agent Name:** stacy-systemproductname (Garuda Linux)
- **Rule Triggered:** 550 - Integrity checksum changed.
- **File Monitored:** `/etc/ssh/sshd_config`
- **Mitre ATT&CK ID:** T1098 (Account Manipulation - SSH Authorized Keys)

### The Payload / Modification
Reviewing the `ossec` logs in Wazuh Threat Hunting, the specific change detected was:

```diff
- # FIM Test Baseline
+ # FIM Test Baseline
+ PermitRootLogin yes
```

The string `PermitRootLogin yes` was appended to the bottom of the SSH configuration, attempting to allow direct remote root access over SSH, bypassing standard user authentication.

## 4. Containment & Eradication
1. **Validation:** Read the `sshd_config` file on the affected endpoint to confirm the modification occurred.
2. **Eradication:** Used `vim` to remove the newly appended `PermitRootLogin yes` line and restored the file to its original state.
3. **Service Restart:** Restarted the SSH daemon (`sudo systemctl restart sshd`) to ensure the malicious configuration was not loaded into active memory.
4. **Credential Audit:** Rotated the `root` user password to ensure the attacker could not immediately re-escalate.

## 5. Lessons Learned & Recommendations
- **Detection Success:** Wazuh's File Integrity Monitoring (FIM) worked perfectly, detecting the baseline deviation within 3 seconds of the write operation.
- **Recommendation:** Implement Wazuh Active Response to automatically revert critical files (like `/etc/ssh/sshd_config`) to their baseline state if an unauthorized modification is detected by FIM, reducing the Mean Time to Respond (MTTR) from 30 minutes to 3 seconds.
