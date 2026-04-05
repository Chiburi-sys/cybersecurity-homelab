#!/usr/bin/env bash
# ============================================================
# Shutdown Alert — Discord Webhook Notifier
# Sends a Discord alert whenever this machine shuts down,
# reboots, or halts — including manual shutdowns.
# ============================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASTE YOUR DISCORD WEBHOOK URL BELOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEBHOOK_URL="https://discord.com/api/webhooks/1489053648058322945/wbuGyiVSehSwutV3iQv3nlXWVYalJvtGAljQ9U7HM9wa6YFeyr4nXqlfT3EyEnVl3Y3d"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Gather system info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOSTNAME=$(hostname)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
UPTIME=$(uptime -p)
USER_WHO=$(who | head -5)
IP_ADDR=$(ip -4 addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -1)

# Detect shutdown type
if systemctl is-system-running --quiet 2>/dev/null; then
    SHUTDOWN_TYPE="Manual Shutdown / Reboot"
else
    SHUTDOWN_TYPE="System Shutdown"
fi

# Check if it's a reboot or full poweroff
if runlevel 2>/dev/null | grep -q '6'; then
    SHUTDOWN_TYPE="🔄 Reboot"
else
    SHUTDOWN_TYPE="⛔ Shutdown / Poweroff"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Build Discord embed payload
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAYLOAD=$(cat <<EOF
{
  "username": "🖥️ System Monitor",
  "avatar_url": "https://raw.githubusercontent.com/wazuh/wazuh/master/src/init/wazuh.png",
  "embeds": [{
    "title": "⚠️ SYSTEM SHUTDOWN ALERT",
    "description": "Your machine **${HOSTNAME}** is going offline.",
    "color": 16744448,
    "fields": [
      {"name": "🖥️ Hostname", "value": "${HOSTNAME}", "inline": true},
      {"name": "🌐 IP Address", "value": "${IP_ADDR:-N/A}", "inline": true},
      {"name": "📋 Type", "value": "${SHUTDOWN_TYPE}", "inline": true},
      {"name": "⏱️ Uptime", "value": "${UPTIME}", "inline": true},
      {"name": "🕐 Timestamp", "value": "${TIMESTAMP}", "inline": false},
      {"name": "👤 Logged-in Users", "value": "\`\`\`${USER_WHO:-None}\`\`\`", "inline": false}
    ],
    "footer": {"text": "Garuda Linux — SOC System Monitor"}
  }]
}
EOF
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Send to Discord
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
curl -s -H "Content-Type: application/json" \
     -d "${PAYLOAD}" \
     "${WEBHOOK_URL}" \
     --max-time 5

exit 0
