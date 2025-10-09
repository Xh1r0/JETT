#!/usr/bin/env python3

import sys
import json
import requests

# Webhook URL dari Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1425706060382994513/xQVAKOfphcb9CIOar4rzK2jTwJfg1NJoNnCiUm9h4Nm7ivBh-ssjLn25h6R_V5F6rJWV"

# Baca input dari Wazuh (stdin)
alert = json.loads(sys.stdin.read())

# Buat isi pesan
message = f"""
🚨 *Wazuh Alert* 🚨
Rule: {alert.get('rule', {}).get('description', 'No description')}
Agent: {alert.get('agent', {}).get('name', 'N/A')}
Severity: {alert.get('rule', {}).get('level', 'N/A')}
Time: {alert.get('timestamp', 'N/A')}
"""

# Kirim ke Discord
payload = {
    "content": message
}

try:
    r = requests.post(WEBHOOK_URL, json=payload)
    r.raise_for_status()
except Exception as e:
    print(f"Failed to send alert: {e}")