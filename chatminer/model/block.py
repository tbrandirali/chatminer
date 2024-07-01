from chatminer.model.message import Message


class Block(object):

    def __init__(self, message: Message = None):
        self.messages = [message]
        self.sender = message.sender

    def __str__(self):
        message_lines = "\n".join(map(lambda msg: f"\t{msg.time} - {msg.text}", self.messages))
        return f"Block(sender='{self.sender}', messages=[\n{message_lines}\n]"
