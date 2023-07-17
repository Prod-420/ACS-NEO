import requests
import time
import json
import socket
import uuid

# Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# Device name
device_name = "Raspberri Pi3b+ Home"

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_mac_address():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    return mac_address

def get_ngrok_url():
    # Make a request to the ngrok API
    res = requests.get('http://localhost:4040/api/tunnels')
    # Parse the JSON response
    res_json = res.json()
    # Get the public URL where ngrok is forwarding HTTP traffic
    url = res_json['tunnels'][0]['public_url']
    return url

def send_to_slack(url):
    # Prepare the message
    message = {
        'text': f'Device: {device_name}\nIP Address: {get_ip_address()}\nMAC Address: {get_mac_address()}\nNew ngrok URL: {url}'
    }
    # Send the message to Slack
    requests.post(slack_webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})

# Remember the last URL we've seen
last_url = None

while True:
    # Get the current ngrok URL
    current_url = get_ngrok_url()

    # If the URL has changed since we last saw it, send a message to Slack
    if current_url != last_url:
        send_to_slack(current_url)
        last_url = current_url

    # Wait for a while before checking again
    time.sleep(30)
