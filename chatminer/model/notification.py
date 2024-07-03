from datetime import datetime

from chatminer import common


class Notification(object):

    def __init__(self, id: int, time: datetime, text: str):
        self.id = id
        self.time = time
        self.text = text

    @staticmethod
    def from_string(id: int, line: str):
        time = datetime.strptime(line.split(' - ', maxsplit=1)[0], '%m/%d/%y, %H:%M')
        text = line.split(' - ', maxsplit=1)[1]
        return Notification(id, time, text)

    def __str__(self):
        return f"{self.time} - '{common.truncate(self.text, 40)}'"
