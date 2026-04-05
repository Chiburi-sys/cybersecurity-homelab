import os
import time

# Ransomware Simulation Script (Safe for Lab)
# This script renames files in a specific directory to simulate encryption alerting.

TARGET_DIR = "./decoy_files"
EXT_NAME = ".crypted"

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
    print(f"[*] Created decoy directory: {TARGET_DIR}")

# Create 10 dummy files
for i in range(1, 11):
    with open(f"{TARGET_DIR}/critical_data_{i}.txt", "w") as f:
        f.write("This is sensitive financial data for lab simulation purposes.")
print(f"[*] Generated 10 dummy files in {TARGET_DIR}")

print("[!] Simulation Starting in 3 seconds... (Mass renaming behavior)")
time.sleep(3)

# Mass rename (Simulating encryption)
files = os.listdir(TARGET_DIR)
for filename in files:
    old_path = os.path.join(TARGET_DIR, filename)
    new_path = old_path + EXT_NAME
    os.rename(old_path, new_path)
    print(f"[!] 'Encrypted' -> {new_path}")

print("\n[+] Simulation Complete.")
print("[+] CHECK YOUR SIEM: Look for 10 File Integrity Monitoring (FIM) events in a short window!")
