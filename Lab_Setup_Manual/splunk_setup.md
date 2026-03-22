# Splunk SIEM Setup — Troubleshooting & Deployment Guide
**Date:** 2026-02-22  
**Analyst:** Stacy  
**Environment:** Ubuntu Server VM (VirtualBox)  
**Splunk Version:** 10.2.0
---
## Overview
This document chronicles the complete setup and troubleshooting process for deploying Splunk Enterprise on Ubuntu Server within a VirtualBox home lab environment. The deployment encountered multiple critical issues related to OpenSSL version mismatches, certificate generation bugs, tmpfs exhaustion, and authentication failures — all of which were systematically resolved.
---
## Initial Environment
| Component      | Detail                            |
|----------------|-----------------------------------|
| Host OS        | Garuda Linux (KDE Plasma)         |
| Hypervisor     | VirtualBox                        |
| Guest OS       | Ubuntu Server                     |
| Static IP      | 192.168.50.10                     |
| Network        | Internal Network (LabNet)         |
| Splunk Version | 10.2.0                           |
---
## Issues Encountered & Solutions
### Issue 1: Splunk Startup Hanging on Certificate Generation
**Symptom:** `sudo /opt/splunk/bin/splunk start` would pass all preliminary checks but hang indefinitely during SSL certificate generation.
**Root Cause:** Multiple compounding issues:
- `/tmp` filesystem was 100% full (tmpfs exhaustion)
- Splunk could not write `splunk.secret` or generate SSL certificates
- OpenSSL version mismatch between Splunk's bundled library and the system
**Solution:**
```bash
# 1. Reboot to clear tmpfs
sudo reboot
# 2. Verify tmpfs is healthy after reboot
df -h
```
---
### Issue 2: OpenSSL Version Mismatch (OPENSSL_3.4.0 Not Found)
**Symptom:**
```
systemctl: /opt/splunk/lib/libcrypto.so.3: version 'OPENSSL_3.4.0' not found
(required by /usr/lib/x86_64-linux-gnu/systemd/libsystemd-shared-257.so)
```
**Root Cause:** Splunk bundles its own OpenSSL library (`/opt/splunk/lib/libcrypto.so.3`) which conflicts with the system's newer OpenSSL version. When `systemctl` runs, it accidentally picks up Splunk's bundled library instead of the system's native one.
**Impact:** `systemctl` and `systemd` commands crash, preventing normal service management.
**Workaround:** Splunk falls back to SysV init scripts (`/etc/init.d/splunk`), but these also trigger the same issue indirectly.
**Solution:** Start Splunk directly using the binary:
```bash
cd /opt/splunk/bin
sudo ./splunk start --accept-license --answer-yes
```
---
### Issue 3: ca.pem Not Found (Known Splunk 10.2.0 Bug)
**Symptom:**
```
The CA file specified (/opt/splunk/etc/auth/cacert.pem) does not exist. Cannot continue.
SSL certificate generation failed.
```
And later:
```
Could not read CA private key from ca.pem
```
**Root Cause:** Splunk 10.2.0's internal certificate generator looks for `ca.pem` in the current working directory. When previous `auth` directory contents were deleted to fix AES-GCM errors, the certificates needed to be regenerated manually.
**Solution:**
```bash
# 1. Generate self-signed CA certificate and private key
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /opt/splunk/etc/auth/privkey.pem \
  -out /opt/splunk/etc/auth/cacert.pem \
  -subj "/CN=SplunkCA"
# 2. Create server.pem (combined cert + key)
sudo bash -c 'cat /opt/splunk/etc/auth/cacert.pem /opt/splunk/etc/auth/privkey.pem > /opt/splunk/etc/auth/server.pem'
# 3. Create ca.pem with BOTH cert and private key (Splunk expects both)
sudo bash -c 'cat /opt/splunk/etc/auth/cacert.pem /opt/splunk/etc/auth/privkey.pem > /opt/splunk/etc/auth/ca.pem'
sudo bash -c 'cat /opt/splunk/etc/auth/cacert.pem /opt/splunk/etc/auth/privkey.pem > /opt/splunk/bin/ca.pem'
sudo bash -c 'cat /opt/splunk/etc/auth/cacert.pem /opt/splunk/etc/auth/privkey.pem > /opt/splunk/ca.pem'
sudo bash -c 'cat /opt/splunk/etc/auth/cacert.pem /opt/splunk/etc/auth/privkey.pem > /ca.pem'
# 4. Fix permissions
sudo chown -R ubuntuuser:ubuntuuser /opt/splunk
sudo chmod -R 755 /opt/splunk
```
---
### Issue 4: AES-GCM Decryption Errors
**Symptom:**
```
AES-GCM Decryption failed!
Decryption operation failed: AES-GCM Decryption failed!
Text decryption - error in finalizing: No errors in queue
```
**Root Cause:** After wiping the `auth` directory, the `splunk.secret` file was regenerated with a new encryption key. Old encrypted passwords stored in Splunk's config files could no longer be decrypted.
**Impact:** Non-fatal. Splunk logs these errors but continues to start normally. The errors are cosmetic for a fresh lab installation.
---
### Issue 5: No Admin Account / Authentication Failure
**Symptom:** Splunk Web displayed `No users exist. Please set up a user.` but provided no way to create one through the UI.
**Root Cause:** The `passwd` file was corrupted/empty after the auth directory was rebuilt.
**Solution:**
```bash
# 1. Stop Splunk
sudo /opt/splunk/bin/splunk stop
# 2. Remove corrupted passwd file
sudo rm -f /opt/splunk/etc/passwd
# 3. Create user-seed.conf to force admin creation
sudo bash -c 'echo -e "[user_info]\nUSERNAME = admin\nPASSWORD = YourPassword!" > /opt/splunk/etc/system/local/user-seed.conf'
# 4. Fix permissions
sudo chown ubuntuuser:ubuntuuser /opt/splunk/etc/system/local/user-seed.conf
# 5. Restart Splunk
sudo /opt/splunk/bin/splunk start
```
When Splunk reads `user-seed.conf` on startup, it creates the admin account and securely removes the password from the file.
---
### Issue 6: Permission Denied on Certificate Generation
**Symptom:**
```
genpkey: Can't open "/opt/splunk/etc/auth/splunkweb/privkey.pem" for writing, Permission denied
```
**Root Cause:** Certificate files were owned by `root` because previous commands used `sudo` and `--run-as-root`. The init script tried to start Splunk as `ubuntuuser`, which couldn't write to root-owned files.
**Solution:**
```bash
sudo chown -R ubuntuuser:ubuntuuser /opt/splunk
sudo chmod -R 755 /opt/splunk
```
---
## Final Working Startup Command
```bash
cd /opt/splunk/bin
sudo ./splunk start --accept-license --answer-yes
```
**Expected Output:**
```
Starting splunk server daemon (splunkd)... Done
Waiting for web server at http://127.0.0.1:8000 to be available.......... Done
The Splunk web interface is at http://UbuntuServer:8000
```
---
## Post-Installation Configuration
### Receiving Port
- **Settings → Forwarding and Receiving → Configure Receiving → New Receiving Port**
- Port: `9997`
### Real-Time Alerts Configured
1. **Brute Force — Multiple Failed Logins** (EventCode 4625 count > 5)
2. **Suspicious Process Execution Detected** (PowerShell, cmd.exe, mshta)
3. **Port Scan Detected** (20+ unique destination ports from single IP)
### SOC Analyst Overview Dashboard
- Failed Login Attempts
- Successful Logins by Account
- Top Processes Created (Sysmon EventCode 1)
- Network Connections by IP & Port (Sysmon EventCode 3)
- Security Event Distribution (Pie chart)
---
## Key Takeaways
1. **Splunk 10.2.0 + Ubuntu's latest OpenSSL = Known compatibility issue.** Plan for manual certificate generation.
2. **Always check disk space (`df -h`) before troubleshooting startup failures.** tmpfs exhaustion causes cryptic, misleading error messages.
3. **File permissions are the silent killer.** After any `sudo` operation on Splunk files, re-run `chown -R`.
4. **The `user-seed.conf` method is the most reliable way to create admin credentials** when the normal first-run prompt fails.
5. **Document everything.** This troubleshooting log became a portfolio asset itself.
---
*This setup guide was created as part of a cybersecurity home lab portfolio. All configurations were performed in an isolated virtual environment.*
