import pandas as pd
import matplotlib.pyplot as plt

from chatminer.model.message import Message


def plot_message_frequency(messages: list[Message], keyword: str) -> None:
    # Isolate timestamps
    timestamps = [message.time for message in messages]
    df = pd.DataFrame(timestamps, columns=['timestamp_column'])

    # Count frequency of entries
    df.set_index('timestamp_column', inplace=True)
    frequency = df.resample('W-MON').size()

    # Plot the frequency data
    plt.figure(figsize=(10, 6))
    frequency.plot(kind='line', marker='', linestyle='-')
    title = f"Frequency of Keyword '{keyword}' Over Time" if keyword else "Frequency of Texts Over Time"
    y_label = "Number of Occurrences" if keyword else "Number of Messages"
    plt.suptitle(title, fontsize=20)
    if keyword:
        plt.title(f"{len(timestamps)} messages in total contain the keyword")
    plt.xlabel('Date', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True)
    plt.show()