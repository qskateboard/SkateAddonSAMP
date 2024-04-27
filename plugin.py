class Plugin:
    def on_connect(self, client):
        pass

    def on_disconnect(self, client):
        pass

    def on_send_chat(self, client, message):
        pass

    def on_send_command(self, client, command):
        pass

    def on_server_message(self, client, color, message):
        pass

    def on_show_dialog(self, client, dialog_id, style, title, button1, button2, text):
        pass
