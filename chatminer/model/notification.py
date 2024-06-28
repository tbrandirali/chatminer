from datetime import datetime


class Notification(object):

    def __init__(self, id: int, time: datetime, text: str):
        self.id = id
        self.time = time
        self.text = text

    @staticmethod
    def from_string(id: int, line: str):
        time = datetime.strptime(line.split(' - ')[0], '%m/%d/%y, %H:%M')
        text = line.split(' - ')[1]
        return Notification(id, time, text)

    def __str__(self):
        return f"Notification(id={self.id}, time={self.time}, text='{self.text}'"
