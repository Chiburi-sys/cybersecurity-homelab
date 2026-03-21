# Wazuh SIEM: Portfolio Screenshot Guide

**Purpose:** Generate high-value, realistic security alerts in Wazuh to capture screenshots for your SOC Analyst portfolio.

---

## Scenario 1: File Integrity Monitoring (FIM) Trigger

*Shows you can track unauthorized modifications to critical system files.*

**The Action:**

1. Open your terminal.
2. We are going to "modify" the SSH configuration file (a common attacker persistence technique). Run this command:

   ```bash
   sudo touch /etc/ssh/sshd_config && sudo echo "# FIM Test" >> /etc/ssh/sshd_config
   ```

**The Screenshot:**

1. Go to your Wazuh Dashboard.
2. Click **File Integrity Monitoring** on the home screen.
3. Click the **Events** tab.
4. Expand the alert that says "*Integrity checksum changed*".
5. **Take Screenshot:** Capture the expanded JSON showing the file path (`/etc/ssh/sshd_config`) and the user who modified it.

---

## Scenario 2: MITRE ATT&CK Mapping & Brute Force

*Shows you understand how alerts map to attacker tactics.*

**The Action:**

1. Open your terminal.
2. We evaluate how the SIEM handles failed logins. Run this command 6 times to simulate a brute force attempt:

   ```bash
   su root
   # (Type an intentionally wrong password like "fake123" and hit Enter)
   ```

**The Screenshot:**

1. Go to your Wazuh Dashboard.
2. Click **MITRE ATT&CK**.
3. Under the "Tactics" matrix, click on **Credential Access**.
4. You should see alerts for *PAM: User authentication failed*.
5. **Take Screenshot:** Capture the MITRE matrix view showing the active tactic and the corresponding alerts below it.

---

## Scenario 3: Suspicious Process Execution

*Shows you monitor for "Living off the Land" binary abuse.*

**The Action:**

1. Open your terminal.
2. We will run a base64 encoded command just like an attacker would:

   ```bash
   bash -c "echo 'cHdk' | base64 -d | sh"
   ```

**The Screenshot:**

1. Go to your Wazuh Dashboard.
2. Click **Security Events**.
3. Go to the **Events** tab.
4. Look for an alert related to anomalous command execution or base64 decoding.
5. **Take Screenshot:** Capture the raw log showing the anomalous command string.

---

## Scenario 4: CIS Benchmark Failure (Configuration Assessment)

*Shows you perform continuous compliance scanning.*

**The Action:**

1. No action needed! Wazuh automatically scans your system when the agent starts.  

**The Screenshot:**

1. Go to your Wazuh Dashboard.
2. Click **Configuration Assessment**.
3. Click on the **CIS benchmark for Arch Linux** (or similar policy).
4. **Take Screenshot:** Capture the dashboard showing the pass/fail ratio and the specific security misconfigurations found on your endpoint.

---

## Final Portfolio Tips

- When taking screenshots, **leave the dark mode enabled** — it looks much more professional and "SOC-like."
- Use the **Threat Hunting** view to show a time-series graph of when these alerts happened alongside the raw logs.
- In your portfolio write-up, frame these screenshots as: *"Demonstrated real-time detection capabilities by simulating MITRE ATT&CK techniques (T1110 Brute Force, T1059 Command Execution) on a monitored endpoint, successfully capturing the resulting alerts in the SIEM."*
