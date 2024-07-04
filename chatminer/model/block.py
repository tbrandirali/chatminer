from chatminer import common
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
        message_lines = "\n".join(
            map(
                lambda msg: f"\t{msg.time} - {common.truncate(msg.text, 50)}",
                self.__messages
            )
        )
        return f"{self.sender}: [\n{message_lines}\n]"
