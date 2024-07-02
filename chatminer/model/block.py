from chatminer.model.message import Message


class Block(object):

    def __init__(self, message: Message = None):
        self.sender = message.sender
        self.__messages = [message]

    def add(self, message: Message = None):
        self.__messages.append(message)

    def get_messages(self) -> list[Message]:
        return self.__messages.copy()

    def __iter__(self):
        for message in self.__messages:
            yield message

    def __len__(self):
        return len(self.__messages)

    def __str__(self) -> str:
        message_lines = "\n".join(map(lambda msg: f"\t{msg.time} - {msg.text}", self.__messages))
        return f"Block(sender='{self.sender}', messages=[\n{message_lines}\n]"
