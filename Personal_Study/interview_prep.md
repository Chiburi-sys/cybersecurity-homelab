# SOC Analyst Interview Preparation — Stacy

This guide translates the technical hands-on projects in this portfolio into conversational "human" answers for cybersecurity interviews. It focuses on the **Why**, the **How**, and the **Lessons Learned**.

---

## 🏢 General & Behavioral

### 1. "Can you walk me through your home lab and why you built it?"

> **Human Answer:** "Sure! I built a complete SOC environment in VirtualBox running four distinct OSes: Kali Linux for attacking, Ubuntu Server for my Splunk SIEM, Windows 11 for the workstation, and Windows Server 2022 as my Domain Controller. On my host machine, I daily-drive **Garuda Linux** (Arch-based), where I run a **Wazuh** manager. I have it configured to start automatically on boot, and I even wrote a custom rule that sends any alerts directly to my **Discord** via a webhook. Even though a leak from a VM to a Linux host is unlikely, I wanted that extra layer of precaution. I built this entire environment because staying in a textbook only goes so far—I wanted to see exactly how these attacks break things and, more importantly, how to fix them when they do."

### 2. "What was the most challenging technical hurdle you faced in this lab?"

> **Human Answer:** "Honestly, it was the initial setup of Splunk 10.2 on Ubuntu Server. There was a weird bug where it conflicted with the system’s OpenSSL version, causing the whole installation to hang during certificate generation. I had to roll up my sleeves and manually generate my own CA, combined certificates, and private keys using `openssl` commands, then manually move them into the `auth` directory. It took a while to troubleshoot and get the pipeline flowing, but it was a great lesson in dependency management—and once I got that hurdle cleared, everything else just clicked into place."

### 3. "How do you stay updated on the latest cyber threats?"

> **Human Answer:** "I’m a big fan of 'The CyberWire' and 'Darknet Diaries' for high-level trends, but for day-to-day stuff, I follow BleepingComputer and the Infosec community on X (Twitter). I also use my lab to recreate things I see in the wild. For example, when I heard about a new password spraying tool, I didn't just read about it—I downloaded it, ran it against my lab's DC, and checked if my existing Splunk alerts could catch it. If they couldn't, I tweaked them until they did."

---

## 🌐 Network Fundamentals

### 4. "Explain the OSI model to me like I’m a non-technical manager."

> **Human Answer:** "Think of it like sending a physical package: The top layers are the actual content (the letter), the middle layers are the envelope and the address, and the bottom layers are the truck and the road it drives on. In a SOC, I mostly live in Layers 3 and 4 (the IP address 'address' and the Port 'door number') and Layer 7 (the actual 'application' data). If an alert fires, I start at the 'truck' (Layer 1/2) to make sure things are plugged in, then work my way up to see if it's a network issue or an actual attack on the 'letter' itself."

### 5. "Why is DNS so important to a SOC analyst?"

> **Human Answer:** "DNS is like the phonebook of the internet. For an attacker, it's a goldmine for 'Command and Control' (C2). If I see a workstation suddenly making a thousand DNS queries to a weird, long domain name like `xyz123-malicious-site.com`, that's a huge red flag for data exfiltration or a beaconing heart-beat. In my lab, I monitor DNS logs specifically to catch these kinds of anomalies."

### 6. "Explain the difference between TCP and UDP like we're at a coffee shop."

> **Human Answer:** "TCP is like a registered letter: you send it, the person signs for it, and sends a confirmation back to you. If you don't hear back, you send it again. It's reliable but slower. UDP is like a postcard: you toss it in the mailbox and hope for the best. It's faster because there's no back-and-forth, but some cards might get lost. In a SOC, I see TCP for things like file transfers and UDP for things like streaming or DNS requests."

---

## 🛡️ SIEM & Detection Engineering

### 7. "How do you differentiate between a Brute Force attack and a Password Spray?"

> **Human Answer:** "In Splunk, I look at the ratio of source IPs to account names. If I see one IP hitting one account a hundred times, that's a brute force. I'd query for a high count of EventCode 4625 for a single user. But if I see one IP hitting *fifty* different accounts only once or twice, that’s a password spray. That’s actually more dangerous because it’s trying to stay under the radar of lockout policies. I wrote specific alerts for both in my lab."

### 8. "Why use both Splunk and Wazuh? Isn't one SIEM enough?"

> **Human Answer:** "I use them for different 'altitudes.' Splunk is my heavy-lifter for Windows Domain logs and centralized search—it's incredibly powerful but expensive in the real world. Wazuh is my XDR/EDR layer. I use it for its built-in File Integrity Monitoring (FIM) and Vulnerability Scanning. If someone touches a sensitive config file on my host, Wazuh catches it instantly with a low overhead. Having both on a resume shows I can work with both industry-standard proprietary tools and powerful open-source alternatives."

### 9. "Explain how you'd detect Kerberoasting in your lab."

> **Human Answer:** "Kerberoasting is a bit sneaky because it looks like a legitimate request for a service ticket. In my lab, I monitor for Windows EventCode 4769. I specifically look for ticket requests where the encryption type is downgraded to RC4 (0x17), which is much easier for an attacker to crack offline. I also set a Service Principal Name (SPN) on a 'honey-pot' service account in my AD setup specifically to trigger this detection."

### 10. "What's the role of Sysmon in your Windows logging strategy?"

> **Human Answer:** "Native Windows logging is okay, but Sysmon is a game-changer. It gives me EventCode 1 (Process Creation) with the full `CommandLine` string. If an attacker runs a base64 encoded PowerShell script, native logs might miss the detail, but Sysmon shows me exactly what was executed. I wouldn't run a SOC without it."

### 11. "How do you handle False Positives in your SIEM?"

> **Human Answer:** "I treat them as 'tuning opportunities.' If an alert fires for a 'Suspicious Admin Script' but it turns out to be our actual IT guy doing a scheduled backup, I don't just ignore it. I'll look at the alert logic in Splunk or Wazuh and add an exclusion for that specific service account or host. The goal isn't to have zero alerts—it's to have high-fidelity alerts so when one fires, I know it's worth my time."

---

## 🚑 Incident Response & Triage

### 12. "Walk me through your triage process when a high-severity alert fires."

> **Human Answer:** "I follow a 'Context First' rule. If a 'Multiple Failed Logins' alert fires, I don't just clear it. I check the source IP—is it coming from the HR manager's laptop at 10:00 AM, or from a Kali Linux box at 3:00 AM? If it's the latter, it's a True Positive. I then correlate: did that IP have any *successful* logins (EventCode 4624) after the failures? If yes, we have a compromise. I'd immediately escalate, document the IOCs, and suggest an account lockout/reset. I’ve documented this exact workflow in my Incident Reports folder."

### 13. "If you found a critical vulnerability on a legacy server that can't be patched, what would you do?"

> **Human Answer:** "I’d look for 'Compensating Controls.' If I can't patch the hole, I'll build a fence around it. That might mean putting the server on a strictly isolated VLAN, adding a specialized WAF (Web Application Firewall) rule in front of it, or cranking up the logging in Wazuh so that the second someone tries to exploit it, I get a high-priority alert. It’s all about risk mitigation when 'the perfect fix' isn't an option."

---

## 📧 Social Engineering & Identity

### 14. "How would you handle a suspected phishing email reported by a user?"

> **Human Answer:** "First, I’d thank the user—they’re our best sensors. Then, I’d isolate the email in a sandbox or a dedicated 'phish-tank.' I’d check the headers for spoofing, scan the links for malicious redirects, and check if any other users in the company received the same mail. If it’s a hit, I’d block the sender’s domain at the gateway and, most importantly, check our logs to see if *anyone* actually clicked. If they did, that's when it turns into an incident."

### 15. "What is MFA (Multi-Factor Authentication), and why isn't it a 'silver bullet'?"

> **Human Answer:** "MFA is the 'something you have' (like a phone app) or 'something you are' (like a thumbprint) on top of 'something you know' (your password). It's great, but it's not perfect. Attackers can bypass it with 'MFA Fatigue' (spamming the user with notifications until they hit 'Accept' out of frustration) or AitM (Adversary-in-the-Middle) proxy attacks. In my lab, I focus on monitoring for suspicious successful logins *even if* MFA was used, because no single control is 100% unhackable."

### 16. "What are the most common ways an attacker gains initial access?"

> **Human Answer:** "It's usually one of three: Phishing (tricking a human), Exploiting a Public-Facing Vulnerability (like an unpatched web server), or using Stolen Credentials (from a previous leak). That’s why I built my lab the way I did—I have a web server to practice vulnerability detection, and I simulate 'Credential Access' attacks like Kerberoasting and Password Spraying to see what those look like in the logs."

---

## 🧠 Analytical & Soft Skills

### 17. "How do you handle a disagreement with a senior analyst about an incident?"

> **Human Answer:** "I’d approach it with data, not ego. If I think something is a critical threat and they don't, I’ll show them the Splunk logs or the Sysmon execution branch that worries me. I’ll ask, 'Can you help me understand why this *isn't* a concern?' It’s about learning their perspective while making sure the risk is properly vetted. At the end of the day, we both want the same thing—to keep the network safe."

### 18. "Where do you see yourself in 5 years in your cyber career?"

> **Human Answer:** "I want to be in a position where I'm not just *reacting* to alerts, but *proactively* hunting for them. I see myself deepening my skills in Detection Engineering—writing complex rules that catch the latest TTPs. I’m also very interested in the automation side of things, like SOAR. I want to be the person who builders the systems that make the whole team faster."

---

## 🚀 Pro Tips for the Interview

- **Be honest about lab limitations:** "I couldn't join my Windows 11 Home VM to the domain because of OS limitations, so I documented it as a known risk and focused on attacking the DC directly."
- **Mention documentation:** "I treat my GitHub READMEs like professional work artifacts because, in a real SOC, if it isn't documented, it didn't happen."
- **Passion project:** Talk about the lab as something you *love* doing, not just a homework assignment. It shows you're a self-learning professional.

---
*Created as part of the SOC Analyst Lab Portfolio. Good luck with your interview!*
