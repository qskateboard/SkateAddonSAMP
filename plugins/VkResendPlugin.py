import time
import requests
import random

from send_command import send_command
from plugin import Plugin


def send_message(peer_id, text):
    payload = {
        "random_id": random.randint(1, 10000000),
        "peer_id": peer_id,
        "message": text,
        "dont_parse_links": "0",
        "disable_mentions": "0",
        "intent": "default",
        "access_token": "",
        "v": "5.131",
    }
    requests.post("https://api.vk.com/method/messages.send", data=payload)


class VkResendPlugin(Plugin):
    def __init__(self):
        self.name = "VkResendPlugin"

    def on_send_command(self, client, command):
        if command.startswith("/vk "):
            send_message("-172773148", command.split(" ", 1)[1])
            send_command(client, "sendMessage", ["Done", 0x00DD00])
