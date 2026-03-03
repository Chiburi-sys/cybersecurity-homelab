# Attack Simulation — Nmap Port Scan
**Date:** 2026-02-28  
**Attacker:** Kali Linux (`192.168.50.30`)  
**Target:** Windows 11 Workstation (`192.168.50.20`)  
**Tool:** Nmap 7.98
---
## Objective
Perform network reconnaissance against the Windows 11 workstation to identify open ports, running services, and potential attack vectors. This simulates the initial phase of a real-world intrusion where an attacker maps the target's attack surface.
---
## MITRE ATT&CK Mapping
| Field     | Value                                     |
|-----------|-------------------------------------------|
| Tactic    | Reconnaissance (TA0043)                   |
| Technique | Active Scanning: Port Scanning (T1595.001)|
| Tactic    | Discovery (TA0007)                        |
| Technique | Network Service Discovery (T1046)         |
---
## Commands Executed
### Scan 1: Full Port Scan with Service Detection
```bash
nmap -A -p- 192.168.50.20
```
- `-A` — Aggressive scan (OS detection, version detection, scripts, traceroute)
- `-p-` — Scan all 65,535 ports
**Result:** All 1,000 scanned ports showed as "ignored states" due to Windows Firewall filtering.
### Scan 2: TCP Connect Scan (Targeted Ports)
```bash
nmap -sT -p 80,443,445,3389,8080 192.168.50.20
```
- `-sT` — TCP Connect scan (completes the full TCP handshake)
- `-p` — Target specific high-value ports
**Result (Firewall ON):**
| Port      | State    | Service          |
|-----------|----------|------------------|
| 80/tcp    | filtered | http             |
| 443/tcp   | filtered | https            |
| 445/tcp   | filtered | microsoft-ds     |
| 3389/tcp  | filtered | ms-wbt-server    |
| 8080/tcp  | filtered | http-proxy       |
All ports were **filtered** — Windows Firewall was blocking the SYN packets before the connection could complete.
### Scan 3: TCP Connect Scan (Firewall Disabled)
```bash
nmap -sT -p 80,443,445,3389,8080 192.168.50.20
```
**Result (Firewall OFF):**
| Port      | State  | Service          |
|-----------|--------|------------------|
| 80/tcp    | closed | http             |
| 443/tcp   | closed | https            |
| 445/tcp   | **open** | microsoft-ds   |
| 3389/tcp  | closed | ms-wbt-server    |
| 8080/tcp  | closed | http-proxy       |
### Scan 4: Top 1000 Ports (Firewall Disabled)
```bash
nmap -sT -p 1-1000 192.168.50.20
```
**Result:**
| Port      | State  | Service          |
|-----------|--------|------------------|
| 135/tcp   | **open** | msrpc           |
| 139/tcp   | **open** | netbios-ssn     |
| 445/tcp   | **open** | microsoft-ds    |
997 ports were closed (connection refused).
---
## Key Findings
1. **Port 445 (SMB)** is open — This is the primary attack vector for file sharing exploits and credential attacks
2. **Port 135 (MSRPC)** is open — Remote Procedure Call service, potential for RPC-based attacks
3. **Port 139 (NetBIOS)** is open — Legacy file sharing protocol, useful for enumeration
4. **Port 3389 (RDP)** is closed — Remote Desktop is not currently enabled
5. **Windows Firewall** effectively blocks all port scans when enabled
---
## Additional Intelligence
- **MAC Address:** `08:00:27:59:D7:8E` (Oracle VirtualBox virtual NIC)
- **Host Latency:** 0.00013s–0.00016s (confirming local network)
- **OS Detection:** Windows 11 detected via SMB banner
---
## Detection in Splunk
### Windows Firewall Log Query
```spl
index=main (EventCode=5156 OR EventCode=5157) "192.168.50.30"
| table _time, EventCode, DestinationAddress, DestinationPort
```
### Sysmon Network Connection Query
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3 SourceIp=192.168.50.30
| stats dc(DestinationPort) as Ports_Scanned, count as Connections by SourceIp
```
> **Note:** The default SwiftOnSecurity Sysmon configuration disables EventCode=3 (Network Connection) to reduce noise. In production environments, consider enabling it selectively for high-value assets.
---
## Lessons Learned
1. **Firewall is critical** — The Windows Firewall completely blocked all scan attempts when enabled
2. **TCP Connect scans (`-sT`) are noisier** but necessary for Sysmon detection since SYN scans don't complete the handshake
3. **Port 445 is the primary target** — SMB is the most commonly exploited Windows service
4. **Scan results vary dramatically** based on firewall state; always document both configurations
---
*This attack simulation was performed in an isolated virtual lab environment for educational purposes only.*
