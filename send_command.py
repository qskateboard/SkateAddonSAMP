import json


def send_command(client, cmd, args=None):
    if args is None:
        args = []
    data = {
        "event": "command",
        "cmd": cmd,
        "args": args
    }
    packet = json.dumps(data)
    packet_length = '{:04}'.format(len(packet))
    client.send(packet_length.encode() + packet.encode())
