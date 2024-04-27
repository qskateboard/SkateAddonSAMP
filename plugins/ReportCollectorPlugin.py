import json
import re
import codecs
from collections import defaultdict
from peewee import *

from send_command import send_command
from plugin import Plugin

# Connect to the database
db = SqliteDatabase('reports.db')


class Report(Model):
    player_nick = CharField()
    report_text = TextField()
    admin_nick = CharField()
    response = TextField()

    class Meta:
        database = db


class ReportCollectorPlugin(Plugin):
    def __init__(self):
        self.name = "ReportCollectorPlugin"
        self.reports = []
        self.current_reports = defaultdict(dict)

        db.connect()
        db.create_tables([Report])

    def on_server_message(self, client, color, message: str):
        if message.startswith("[Жалоба]"):
            result1 = re.findall(r'\[Жалоба\] от (.*?)\[.*?]:{FFFFFF} (.*?)\. У', message)

            report_text = result1[0][1]
            player_nick = result1[0][0]
            self.current_reports[player_nick] = {"report_text": report_text, "player_nick": player_nick}

        elif message.startswith("[A]") and " -> " in message:
            result2 = re.findall(r'\[A\] (\w+_\w+)[\d\[\]]+ -> (\w+_\w+)[\d\[\]]+:{FFFFFF}(.*)', message)

            admin_nick = result2[0][0]
            response = result2[0][2]
            player_nick = result2[0][1]
            try:
                report_text = self.current_reports[player_nick]['report_text']
                self.current_reports[player_nick].update({"admin_nick": admin_nick, "response": response})

                # Save reports to the database
                report = Report(player_nick=player_nick, report_text=report_text, admin_nick=admin_nick, response=response)
                report.save()
                send_command(client, "sendMessage",
                             ["Added new report to database {E5261A}[" + player_nick + "/" + admin_nick + "]", 0xFFFFFF])

                del self.current_reports[player_nick]
            except:
                pass
