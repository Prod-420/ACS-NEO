import requests
import time
import json
import socket
import uuid

# Slack webhook URL
slack_webhook_url = 'https://your_slack_Tocken'

# Device name
device_name = "My Device"

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f'IP Address: {ip_address}')
    return ip_address

def get_mac_address():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    print(f'MAC Address: {mac_address}')
    return mac_address

def get_ngrok_url():
    # Make a request to the ngrok API
    res = requests.get('http://localhost:4040/api/tunnels')
    # Parse the JSON response
    res_json = res.json()
    # Get the public URL where ngrok is forwarding HTTP traffic
    for tunnel in res_json['tunnels']:
        url = tunnel['public_url']
        if url.startswith('https'):
            print(f'ngrok URL: {url}')
            return url
    return None

def send_to_slack(url):
    # Prepare the message
    message = {
        'text': f'Device: {device_name}\nIP Address: {get_ip_address()}\nMAC Address: {get_mac_address()}\nNew ngrok URL: {url}'
    }
    # Send the message to Slack
    response = requests.post(slack_webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print('Message sent to Slack')
    else:
        print(f'Failed to send message to Slack, status code: {response.status_code}, response: {response.text}')

 # Remember the last URL we've seen
last_url = None

while True:
    # Get the current ngrok URL
    current_url = get_ngrok_url()

    # If the URL has changed since we last saw it, send a message to Slack
    if current_url != last_url:
        print('URL has changed. Sending new URL to Slack.')
        send_to_slack(current_url)
        last_url = current_url

    # Wait for a while before checking again
    time.sleep(30)
