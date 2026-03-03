#!/usr/bin/env python3
"""
Failed Login Analyzer
Parses Windows Security event log CSV exports from Splunk
to identify brute force and password spray patterns.

Usage:
    python3 failed_login_parser.py <splunk_export.csv>

Expected CSV columns (Splunk export):
    _time, EventCode, Account_Name, Source_Network_Address, Failure_Reason
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime


def parse_failed_logins(filepath):
    """Parse a Splunk CSV export of EventCode 4625 events."""
    
    logins_by_ip = defaultdict(list)
    logins_by_account = defaultdict(list)
    total_events = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                event_code = row.get('EventCode', '').strip()
                if event_code != '4625':
                    continue
                
                total_events += 1
                timestamp = row.get('_time', 'Unknown')
                account = row.get('Account_Name', 'Unknown')
                source_ip = row.get('Source_Network_Address', 'Unknown')
                reason = row.get('Failure_Reason', 'Unknown')
                
                event = {
                    'time': timestamp,
                    'account': account,
                    'source_ip': source_ip,
                    'reason': reason
                }
                
                logins_by_ip[source_ip].append(event)
                logins_by_account[account].append(event)
    
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    except KeyError as e:
        print(f"[ERROR] Missing expected column: {e}")
        print("Expected columns: _time, EventCode, Account_Name, Source_Network_Address, Failure_Reason")
        sys.exit(1)
    
    return total_events, logins_by_ip, logins_by_account


def detect_brute_force(logins_by_ip, threshold=5):
    """Identify IPs with failed logins exceeding the threshold."""
    
    suspects = {}
    for ip, events in logins_by_ip.items():
        if len(events) >= threshold:
            accounts_targeted = set(e['account'] for e in events)
            suspects[ip] = {
                'count': len(events),
                'accounts': accounts_targeted,
                'first_seen': events[0]['time'],
                'last_seen': events[-1]['time']
            }
    return suspects


def detect_password_spray(logins_by_ip, account_threshold=3):
    """Identify IPs targeting multiple accounts (spray pattern)."""
    
    sprayers = {}
    for ip, events in logins_by_ip.items():
        unique_accounts = set(e['account'] for e in events)
        if len(unique_accounts) >= account_threshold:
            sprayers[ip] = {
                'count': len(events),
                'unique_accounts': len(unique_accounts),
                'accounts': unique_accounts,
                'first_seen': events[0]['time'],
                'last_seen': events[-1]['time']
            }
    return sprayers


def print_report(total, logins_by_ip, logins_by_account, suspects, sprayers):
    """Print a formatted analysis report."""
    
    print("=" * 60)
    print("  FAILED LOGIN ANALYSIS REPORT")
    print("=" * 60)
    print(f"\n  Total Failed Login Events (4625): {total}\n")
    
    # --- Top Source IPs ---
    print("-" * 60)
    print("  TOP SOURCE IPs")
    print("-" * 60)
    sorted_ips = sorted(logins_by_ip.items(), key=lambda x: len(x[1]), reverse=True)
    for ip, events in sorted_ips[:10]:
        accounts = set(e['account'] for e in events)
        print(f"  {ip:<20} {len(events):>5} failures  ({len(accounts)} accounts)")
    
    # --- Top Targeted Accounts ---
    print(f"\n{'-' * 60}")
    print("  TOP TARGETED ACCOUNTS")
    print("-" * 60)
    sorted_accounts = sorted(logins_by_account.items(), key=lambda x: len(x[1]), reverse=True)
    for account, events in sorted_accounts[:10]:
        sources = set(e['source_ip'] for e in events)
        print(f"  {account:<20} {len(events):>5} failures  (from {len(sources)} IPs)")
    
    # --- Brute Force Alerts ---
    if suspects:
        print(f"\n{'=' * 60}")
        print("  ⚠️  BRUTE FORCE DETECTED")
        print("=" * 60)
        for ip, info in suspects.items():
            print(f"\n  Source IP: {ip}")
            print(f"  Failures: {info['count']}")
            print(f"  Accounts: {', '.join(info['accounts'])}")
            print(f"  Window:   {info['first_seen']} → {info['last_seen']}")
    
    # --- Password Spray Alerts ---
    if sprayers:
        print(f"\n{'=' * 60}")
        print("  ⚠️  PASSWORD SPRAY DETECTED")
        print("=" * 60)
        for ip, info in sprayers.items():
            print(f"\n  Source IP: {ip}")
            print(f"  Failures: {info['count']} across {info['unique_accounts']} accounts")
            print(f"  Accounts: {', '.join(info['accounts'])}")
            print(f"  Window:   {info['first_seen']} → {info['last_seen']}")
    
    if not suspects and not sprayers:
        print(f"\n  ✅ No brute force or password spray patterns detected.")
    
    print(f"\n{'=' * 60}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 failed_login_parser.py <splunk_export.csv>")
        print("\nExport from Splunk with:")
        print('  index=main EventCode=4625')
        print('  | table _time, EventCode, Account_Name, Source_Network_Address, Failure_Reason')
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"\n[*] Analyzing: {filepath}\n")
    
    total, logins_by_ip, logins_by_account = parse_failed_logins(filepath)
    
    if total == 0:
        print("[!] No EventCode 4625 events found in the file.")
        sys.exit(0)
    
    suspects = detect_brute_force(logins_by_ip, threshold=5)
    sprayers = detect_password_spray(logins_by_ip, account_threshold=3)
    
    print_report(total, logins_by_ip, logins_by_account, suspects, sprayers)


if __name__ == "__main__":
    main()
