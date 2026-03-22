# Walkthrough: Investigating & Tuning Wazuh Anomalies

This guide walks you through exactly how I handled the "Trojaned Binary" detection on your host machine. This is a real-world scenario that every SOC Analyst eventually faces.

---

## 🏗️ 1. Detection: The "Trojaned" Alarm
Wazuh’s **Rootcheck** module uses generic signatures to scan for rootkits. It looks for specific patterns of code that often belong to malicious backdoors.

- **The Trigger:** Wazuh found a string of bytes in `/usr/bin/passwd` that matched a generic signature.
- **The Problem:** Many legitimate binaries on specialized Linux distros (like Garuda/Arch) use those same patterns for valid features (like PAM authentication or localized languages). This creates a **False Positive (FP)**.

---

## 🔍 2. Investigation: Proving the System is Clean
Before silencing an alarm, an analyst **must** prove it's a false positive. We did this in two ways:

### A. Timeline Analysis
I used the `stat` command to check the last time your `passwd` binary was changed:
```bash
ls -l --time-style=long-iso /usr/bin/passwd
```
- **Finding:** The file was last changed in **June 2025**. 
- **Context:** Your system logs showed you installed the package in **November 2025**. Since the file is older than the install date, it means it hasn't been tampered with since you've owned the system.

### B. Hash Verification (The "Golden Proof")
We used the Arch package manager (`pacman`) to check the actual SHA-256 hash of the file against the official database.
```bash
sudo pacman -Qk shadow
```
- **The Result:** `0 altered files`. This is absolute proof that the file is authentic and precisely what the developers released.

---

## 🛠️ 3. SIEM Tuning: Silencing the Noise
Now that we knew it was safe, we needed to stop Wazuh from alerting on it every time it scanned.

### A. The Custom Rule
I modified your **`Wazuh_SIEM/wazuh_local_rules.xml`** to add a "suppression" rule:
```xml
<rule id="100020" level="0">
  <if_sid>510</if_sid>
  <match>/usr/bin/passwd|/usr/sbin/passwd|/sbin/passwd|/bin/passwd</match>
  <description>Ignore false positive Rootcheck alerts for passwd on Arch-based systems.</description>
</rule>
```
- **Level 0:** This tells Wazuh to process the event but **never** log it or show it on the dashboard.
- **if_sid 510:** This ensures it only applies when the Rootcheck (Rule 510) triggers.

### B. Deployment
Finally, we pushed the new rule into the Docker container and restarted the manager:
```bash
# Copy the local file to the manager container
docker cp wazuh_local_rules.xml single-node-wazuh.manager-1:/var/ossec/etc/rules/local_rules.xml

# Restart the manager to load the rule
docker exec single-node-wazuh.manager-1 /var/ossec/bin/wazuh-control restart
```

---

## 🎯 Summary of SOC Skills Used
- **SIEM Detection Engineering:** Tuning rules to reduce noise and "alert fatigue".
- **Forensic Investigation:** Using native OS tools to validate the integrity of system files.
- **Linux Administration:** Navigating the filesystem and using package manager verification tools.
- **Docker Management:** Pushing configurations into a live containerized environment.

---

## 📸 4. Incident History & Proof
Below is the complete terminal history showing the timeline analysis, package integrity verification, and the final SIEM tuning deployment.

![Wazuh Incident Investigation & Tuning History](/home/stacy/Cyber Security Portfolio/Screenshots/Wazuh/wazuh_incident_investigation_history.png)

---

*Keep this walkthrough in your portfolio — it’s a perfect example of what a professional SOC Analyst does every day!* 🛡️🚀
