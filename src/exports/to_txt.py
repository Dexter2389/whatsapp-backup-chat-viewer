from datetime import datetime
from typing import Callable, Generator, List

from ..models import CallLog, Chat, Contact, GroupName, Message


def chats_to_txt_raw(chat: Chat, dir: str) -> None:
    """Store chat messages in a text file without formatting.

    Args:
        chat (Chat): Chat to be formatted.
        dir (str): Directory to write the formatted chat.

    Returns:
        None: Creates .txt file of the chat in the given directory
    """

    if isinstance(chat.chat_title, Contact):
        if chat.chat_title.name and chat.chat_title.number:
            chat_title_details = f"{chat.chat_title.name} ({chat.chat_title.number})"
        else:
            chat_title_details = f"+{chat.chat_title.raw_string_jid.split('@')[0]}"
    elif isinstance(chat.chat_title, GroupName):
        chat_title_details = f"{chat.chat_title.name}"
    else:
        chat_title_details = ""

    messages = "\n".join([str(message) for message in chat.messages])
    with open(f"{dir}/{chat_title_details}-raw.txt", "w") as file:
        file.write(f"{chat_title_details}\n\n{messages}")


def chats_to_txt_formatted(chat: Chat, dir: str) -> None:
    """Format chat messages in a readable format and store them as a text file.

    Args:
        chat (Chat): Chat to be formatted.
        dir (str): Directory to write the formatted chat.

    Returns:
        None: Creates .txt file of the chat in the given directory
    """
    message_list = []

    def resolve_sender_name(message: Message) -> str:
        """Utility function to extract 'sender_name' from a given message.

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

        Yields:
            Message: Message object to which the reply was given.
        """
        for ct in chat_list:
            if compare_function(ct):
                yield ct

    for idx, message in enumerate(chat.messages):
        date_time = datetime.fromtimestamp(int(message.timestamp) / 1000)
        if (
            not message.text_data
            and not message.reply_to
            and not message.media
            and not message.geo_position
        ):
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
                    elif orig_message.geo_position:
                        orig_message_data_str = f"location: ({orig_message.geo_position.latitude},{orig_message.geo_position.longitude})"
                    else:
                        orig_message_data_str = ""
                    message_str += f"\n\t>>> Reply to: {resolve_sender_name(orig_message)} - {orig_message_data_str}"
                else:
                    message_str += "\n\t>>> Reply to: 'Message has been deleted'"

            # Retrieve media from the message if any
            if message.media:
                message_str += f"\n\t>>> Media: {message.media.file_path}"

            # Retrieve location from the message if any
            if message.geo_position:
                message_str += f"\n\t>>> Location: ({message.geo_position.latitude},{message.geo_position.longitude})"

        message_list.append(message_str)

    if isinstance(chat.chat_title, Contact):
        if chat.chat_title.name and chat.chat_title.number:
            chat_title_details = f"{chat.chat_title.name} ({chat.chat_title.number})"
        else:
            chat_title_details = f"+{chat.chat_title.raw_string_jid.split('@')[0]}"
    elif isinstance(chat.chat_title, GroupName):
        chat_title_details = f"{chat.chat_title.name}"
    else:
        chat_title_details = ""

    messages = "\n".join(message_list)
    with open(f"{dir}/{chat_title_details}.txt", "w") as file:
        file.write(f"{chat_title_details}\n\n{messages}")


def call_logs_to_txt_raw(call_log: CallLog, dir: str) -> None:
    """Store call logs in a text file without formatting.

    Args:
        call_log (CallLog): CallLog to be formatted.
        dir (str): Directory to write the formatted call log.

    Returns:
        None: Creates .txt file of the call log in the given directory.
    """
    if call_log.caller_id.name and call_log.caller_id.number:
        caller_id_details = f"{call_log.caller_id.name} ({call_log.caller_id.number})"
    else:
        caller_id_details = f"+{call_log.caller_id.raw_string_jid.split('@')[0]}"

    call_logs = "\n".join([str(call) for call in call_log.calls])
    with open(f"{dir}/{caller_id_details}-raw.txt", "w") as file:
        file.write(f"{caller_id_details}\n\n{call_logs}")


def call_logs_to_txt_formatted(call_log: CallLog, dir: str) -> None:
    """Format call logs in a readable format and store them as a text file.

    Args:
        call_log (CallLog): CallLog to be formatted.
        dir (str): Directory to write the formatted call log.

    Returns:
        None: Creates .txt file of the call log in the given directory.
    """
    call_log_list = []

    def seconds_to_hms(duration_in_sec: int) -> str:
        """Convert seconds to hours, minutes and seconds for better representation.

        Args:
            duration_in_sec (int): duration in seconds

        Returns:
            str: Either hours, minutes or seconds based on the converted duration.
        """
        hours = (duration_in_sec // 3600) % 24
        minutes = (duration_in_sec // 60) % 60
        seconds = duration_in_sec % 60

        if hours != 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d} hours"
        elif minutes != 0:
            return f"{minutes:02d}:{seconds:02d} minutes"
        else:
            return f"{seconds:02d} seconds"

    if call_log.caller_id.name and call_log.caller_id.number:
        caller_id_details = f"{call_log.caller_id.name} ({call_log.caller_id.number})"
    else:
        caller_id_details = f"+{call_log.caller_id.raw_string_jid.split('@')[0]}"

    for call in call_log.calls:
        date_time = datetime.fromtimestamp(int(call.timestamp) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if call.from_me:
            call_log_str = (
                f"[{date_time}]: Me ----> {caller_id_details}\n\t>>> Call Type: 📹 - Video Call\n\t>>> Duration: {seconds_to_hms(duration_in_sec=call.duration)}\n\t>>> Status: {call.call_result}"
                if call.video_call
                else f"[{date_time}]: Me ----> {caller_id_details}\n\t>>> Call Type: 📞 - Voice Call\n\t>>> Duration: {seconds_to_hms(duration_in_sec=call.duration)}\n\t>>> Status: {call.call_result}"
            )
        else:
            call_log_str = (
                f"[{date_time}]: {caller_id_details} ----> Me\n\t>>> Call Type: 📹 - Video Call\n\t>>> Duration: {seconds_to_hms(duration_in_sec=call.duration)}\n\t>>> Status: {call.call_result}"
                if call.video_call
                else f"[{date_time}]: {caller_id_details} ----> Me\n\t>>> Call Type: 📞 - Voice Call\n\t>>> Duration: {seconds_to_hms(duration_in_sec=call.duration)}\n\t>>> Status: {call.call_result}"
            )

        call_log_list.append(call_log_str)

    call_logs = "\n".join(call_log_list)
    with open(f"{dir}/{caller_id_details}.txt", "w") as file:
        file.write(f"{caller_id_details}\n\n{call_logs}")
