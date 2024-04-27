import json
import socket
import os
import importlib

from plugin import Plugin


HOST, PORT = "127.0.0.1", 1337


class Main:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        self.plugins.clear()  # Clear the existing plugin instances
        files = os.listdir("plugins")
        for file in files:
            if file.endswith(".py"):
                module = importlib.reload(importlib.import_module(f"plugins.{file[:-3]}"))
                for class_name in dir(module):
                    if class_name != "Plugin" and type(getattr(module, class_name)) == type:
                        if issubclass(getattr(module, class_name), Plugin):
                            plug = getattr(module, class_name)()
                            print("[Core] Loaded plugin " + plug.name)
                            self.plugins.append(plug)

    def run(self):
        self.load_plugins()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print("Listening for connections on {}:{}".format(HOST, PORT))

        while True:
            client, address = server.accept()
            print("Client connected from {}".format(address))
            # Notify the plugin instances of the connection
            for plugin in self.plugins:
                plugin.on_connect(client)

            while True:
                try:
                    try:
                        packet_length = int(client.recv(4))
                    except ValueError:
                        print("Error: received empty packet_length")
                        break

                    packet = b''
                    while packet_length:
                        data = client.recv(packet_length)
                        packet_length -= len(data)
                        packet += data

                        data = json.loads(packet.decode(errors='ignore', encoding='cp1251'))
                        print(data)
                        event = data["event"]
                        args = data["args"]

                        if event == "onSendChat":
                            message = args[0]
                            for plugin in self.plugins:
                                plugin.on_send_chat(client, message)

                        elif event == "onSendCommand":
                            command = args[0]

                            if "/skate.reload" in command:
                                self.load_plugins()
                                continue

                            if "/skate.plugins" in command:
                                from send_command import send_command
                                send_command(client, "sendMessage", ["List of active plugins:", 0x00DD00])
                                plugins_list = [send_command(client, "sendMessage", [plg.name, 0xFFFFFF]) for plg in self.plugins]
                                continue

                            for plugin in self.plugins:
                                plugin.on_send_command(client, command)

                        elif event == "onServerMessage":
                            color, message = args
                            for plugin in self.plugins:
                                plugin.on_server_message(client, color, message)

                        elif event == "onShowDialog":
                            dialog_id, style, title, button1, button2, text = args
                            for plugin in self.plugins:
                                plugin.on_show_dialog(client, dialog_id, style, title, button1, button2, text)

                        else:
                            print("Unknown event: {}".format(event))
                except Exception as e:
                    print("Error: ", e)
                    break


if __name__ == "__main__":
    Main().run()
