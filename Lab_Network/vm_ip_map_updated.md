# Updated VM IP Address Map

All VMs are configured with **static IP addresses** on the VirtualBox **Internal Network (LabNet)**.

- **Network:** LabNet
- **Subnet:** 192.168.50.0/24
- **Gateway:** 192.168.50.1

---

## VM IP Address Table

| Hostname           | Role                  | Operating System              | Static IP       | Notes |
|--------------------|-----------------------|-------------------------------|-----------------|-------|
| WindowsServer2022  | Domain Controller     | Windows Server 2022 Standard  | 192.168.50.5    | AD DS, DNS Server, Splunk Forwarder |
| UbuntuServer       | Splunk SIEM           | Ubuntu Server                 | 192.168.50.10   | Splunk Enterprise; receives logs from all Windows hosts |
| Win11              | Domain Workstation    | Windows 11                    | 192.168.50.20   | Sysmon installed; domain-joined |
| Kali               | Attack Machine        | Kali Linux                    | 192.168.50.30   | Offensive security simulations |
