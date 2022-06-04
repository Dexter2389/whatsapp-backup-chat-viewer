from datetime import datetime
from typing import Callable, Generator, List

from .models import Chat, Message


def chats_to_txt_raw(chat: Chat, dir: str) -> None:
    messages = "\n".join([str(message) for message in chat.messages])
    with open(f"{dir}/{chat.chat_title.name}-raw.txt", "w") as file:
        file.write(f"{chat.chat_title.name}\n\n{messages}")


def chats_to_txt_formatted(chat: Chat, dir: str) -> None:
    message_list = []

    def resolve_sender_name(message: Message) -> str:
        """Utility function to extract sender_name from a given message.

        Args:
            message (Message): Message from which we want to extract sender_name.

        Returns:
            str: sender_name
        """
        if message.from_me:
            sender_name = "Me"
        else:
            sender_name = (
                message.sender_contact.name
                if message.sender_contact.name is not None
                else message.sender_contact.raw_string_jid[
                    : message.sender_contact.raw_string_jid.index("@")
                ]
            )
        return sender_name

    def find_reply(
        compare_function: Callable, chat_list: List[Message]
    ) -> Generator[Message, None, None]:
        """Generator function to find the message to which a reply was given.

        Args:
            compare_function (function): Compare lambda function that needs to be run against the chat_list.
            chat_list (List[Message]): List of chat messages.
        """
        for chat in chat_list:
            if compare_function(chat):
                yield chat

    for idx, message in enumerate(chat.messages):
        date_time = datetime.fromtimestamp(int(message.timestamp) / 1000)
        if not message.text_data and not message.reply_to and not message.media:
            # If there is no data or media or reply_to, we can assume that the message was about change in chat settings.
            message_str = f"[{date_time}] 'Change in the chat settings'"
        else:
            sender_name = resolve_sender_name(message=message)

            message_str = (
                f"[{date_time}]: {sender_name} - {message.text_data}"
                if message.text_data
                else f"[{date_time}]: {sender_name}"
            )

            # Retrieve the 'original message' to which the replied message belongs to.
            if message.reply_to:
                orig_message = next(
                    find_reply(
                        lambda x: message.reply_to == x.key_id,
                        chat.messages[:idx],
                    ),
                    None,
                )  # Get the original message.

                # Check if the reply is given to a deleted message
                # If orig_message is None, we can assume that the original message was deleted
                if orig_message:
                    if orig_message.text_data:
                        orig_message_data_str = " ".join(
                            orig_message.text_data.splitlines()
                        )
                    elif orig_message.media:
                        orig_message_data_str = f"media: {orig_message.media.file_path}"
                    message_str += f"\n\t>>> Reply to: {resolve_sender_name(orig_message)} - {orig_message_data_str}"
                else:
                    message_str += "\n\t>>> Reply to: 'Message has been deleted'"

            # Retrieve media from the message if any
            if message.media:
                message_str += f"\n\t>>> Media: {message.media.file_path}"

        message_list.append(message_str)

    messages = "\n".join(message_list)
    with open(f"{dir}/{chat.chat_title.name}.txt", "w") as file:
        file.write(f"{chat.chat_title.name}\n\n{messages}")
