import time

from send_command import send_command
from plugin import Plugin


class TestPlugin(Plugin):
    def __init__(self):
        self.name = "TestPlugin"

    def on_connect(self, client):
        print("Connected new client")

    def on_send_chat(self, client, message):
        if message == "hello":
            time.sleep(0.3)
            send_command(client, "sendMessage", ["hello there", 0x00DD00])
