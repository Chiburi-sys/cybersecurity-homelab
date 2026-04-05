import discord
import subprocess
import os
import json

# Token must never be committed. Set DISCORD_BOT_TOKEN (see discord-bot.env.example).
TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit(
        "Set DISCORD_BOT_TOKEN in the environment (e.g. Scripts/discord-bot.env for systemd)."
    )

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Helper function to run shell commands safely
    def run_cmd(cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return str(e)

    # ===============
    # !help COMMAND
    # ===============
    if message.content.startswith('!help'):
        help_text = (
            "🛠️ **Homelab SOC Bot Commands** 🛠️\n"
            "`!status`    - Show system vitals and Wazuh Agent status\n"
            "`!services`  - View live Wazuh Docker SIEM cluster status\n"
            "`!alerts`    - Fetch the 3 most recent SIEM alerts directly from the Manager\n"
            "`!scan`      - Check if the Wazuh Agent initial baseline scan is finished\n"
            "`!help`      - Display this help message"
        )
        await message.channel.send(help_text)

    # ===============
    # !status COMMAND
    # ===============
    elif message.content.startswith('!status'):
        uptime = run_cmd("uptime -p")
        agent_status = run_cmd("systemctl is-active wazuh-agent")
        if agent_status == "active":
            agent_color = "🟢 Active"
        else:
            agent_color = "🔴 Offline"

        embed = discord.Embed(title="📊 Host System Status", color=discord.Color.blue())
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.add_field(name="Wazuh Host Agent", value=agent_color, inline=False)
        
        await message.channel.send(embed=embed)

    # ===============
    # !services COMMAND
    # ===============
    elif message.content.startswith('!services'):
        res = run_cmd("docker compose -f /home/stacy/wazuh-docker/single-node/docker-compose.yml ps --format 'table {{.Service}}\t{{.Status}}'")
        if not res:
            res = "No docker containers running or Docker is down."
            
        embed = discord.Embed(title="🐳 SIEM Cluster Status", description=f"```\n{res}\n```", color=discord.Color.green())
        await message.channel.send(embed=embed)

    # ===============
    # !alerts COMMAND
    # ===============
    elif message.content.startswith('!alerts'):
        # Just grab the last 3 parsed alerts
        cmd = "docker exec single-node-wazuh.manager-1 tail -n 100 /var/ossec/logs/alerts/alerts.json"
        out = run_cmd(cmd)
        alerts_found = []
        
        for line in out.splitlines():
            try:
                alert = json.loads(line)
                rule = alert.get("rule", {})
                level = rule.get("level", 0)
                desc = rule.get("description", "Unknown")
                id = rule.get("id", "N/A")
                if level >= 3:  # Only grab meaningful alerts
                    alerts_found.append(f"Level {level} (Rule {id}): {desc}")
            except:
                pass
                
        # Send the last 3 
        recent = alerts_found[-3:] if alerts_found else ["No recent high-level alerts found."]
        resp = "\n".join(recent)
        
        embed = discord.Embed(title="🚨 Recent Security Alerts", description=f"```\n{resp}\n```", color=discord.Color.orange())
        await message.channel.send(embed=embed)

    # ===============
    # !scan COMMAND
    # ===============
    elif message.content.startswith('!scan'):
        cmd = "echo 4255 | sudo -S grep 'File integrity monitoring scan' /var/ossec/logs/ossec.log | tail -n 1"
        out = run_cmd(cmd)
        
        if "scan ended" in out:
            statusMsg = "✅ **Scan Completed!** Real-time monitoring is active."
            color = discord.Color.green()
        elif "scan started" in out:
            statusMsg = "⏳ **Scanning in progress...** Real-time monitoring is currently paused."
            color = discord.Color.gold()
        else:
            statusMsg = "❔ **Unknown status.** Cannot determine scan state."
            color = discord.Color.red()

        embed = discord.Embed(title="🔍 FIM Baseline Status", description=statusMsg, color=color)
        await message.channel.send(embed=embed)


client.run(TOKEN)
