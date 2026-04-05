#!/usr/bin/env python3
import sys
import json
import logging
import urllib.request
import urllib.error

# Logger configuration
logging.basicConfig(filename='/var/ossec/logs/integrations.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def main():
    if len(sys.argv) < 4:
        logging.error("Invalid arguments: %s", sys.argv)
        sys.exit(1)

    alert_file_location = sys.argv[1]
    hook_url = sys.argv[3]

    try:
        with open(alert_file_location) as alert_file:
            alert = json.load(alert_file)
    except Exception as e:
        logging.error("Could not read alert file: %s", e)
        sys.exit(1)

    # Extract alert properties
    rule = alert.get('rule', {})
    rule_id = str(rule.get('id', 'N/A'))
    level = rule.get('level', 'N/A')
    description = rule.get('description', 'No description provided')
    agent = alert.get('agent', {})
    agent_name = agent.get('name', 'N/A')
    
    # Active Response Context
    is_active_response = 'Active response' in description
    
    color = 16711680 # Red for standard high alerts
    if is_active_response:
        color = 65280 # Green for an active response mitigating a threat

    embed = {
        "title": f"🚨 Wazuh Alert: {description}" if not is_active_response else f"🛡️ Wazuh SOC: Automated Remediation Taken!",
        "color": color,
        "fields": [
            {"name": "Severity Level", "value": str(level), "inline": True},
            {"name": "Rule ID", "value": rule_id, "inline": True},
            {"name": "Agent", "value": agent_name, "inline": False}
        ],
        "footer": {"text": "Wazuh SIEM - SOC Automation"}
    }

    # If it's a brute force or an active response, add mitigation suggestions
    if rule_id in ['5712', '5720']:
        embed["fields"].append({"name": "🎯 SOC Suggestion", "value": "A brute-force attack was detected. Wazuh has automatically triggered the firewall-drop script to block the source IP for 10 minutes.", "inline": False})
    elif is_active_response:
        command = alert.get('parameters', {}).get('command', 'unknown command')
        embed["fields"].append({"name": "🛠️ Action Taken", "value": f"Wazuh executed the `{command}` script locally on {agent_name} to stop the threat.", "inline": False})
        embed["fields"].append({"name": "🎯 SOC Suggestion", "value": "Review the preceding alerts to confirm what triggered this mitigation. No immediate action required, threat contained.", "inline": False})
    else:
        embed["fields"].append({"name": "🎯 SOC Suggestion", "value": "Investigate this alert in the Wazuh Threat Hunting dashboard.", "inline": False})

    payload = {
        "username": "Wazuh SOC Analyst",
        "avatar_url": "https://raw.githubusercontent.com/wazuh/wazuh/master/src/init/wazuh.png",
        "embeds": [embed]
    }

    req = urllib.request.Request(hook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 204]:
                logging.info("Successfully sent alert %s to Discord", rule_id)
            else:
                logging.error("Failed to send alert to Discord: %s", response.status)
    except urllib.error.HTTPError as e:
        logging.error("Failed to send alert to Discord: %s - %s", e.code, e.read().decode())
    except urllib.error.URLError as e:
        logging.error("Failed to connect to Discord URL: %s", e.reason)

if __name__ == "__main__":
    main()
