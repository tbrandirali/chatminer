from datetime import datetime


class Message(object):

    def __init__(self, id: int, time: datetime, sender: str, text: str):
        self.id = id
        self.time = time
        self.sender = sender
        self.text = text

    @staticmethod
    def from_string(id: int, line: str):
        time = datetime.strptime(line.split(' - ')[0], '%m/%d/%y, %H:%M')
        sender = line.split(' - ', maxsplit=1)[1].split(':')[0]
        text = line.split(' - ', maxsplit=1)[1].split(': ')[1]
        return Message(id, time, sender, text)

    def __str__(self):
        return f"Message(id={self.id}, time={self.time}, sender={self.sender}, text='{self.text}'"
