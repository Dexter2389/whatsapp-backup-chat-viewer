import json

from attrs import asdict

from ..models import CallLog, Chat, Contact, GroupName


def chats_to_json(chat: Chat, dir: str) -> None:
    """Store chat as a JSON file.

    It takes a chat object and a directory, and writes a json file to the directory with the chat's
    title as the file name

    Args:
        chat (Chat): Chat - the chat object to be converted to JSON
        dir (str): The directory to save the chats to.

    Returns:
        None: Creates .json file of the chat in the given directory
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

    with open(f"{dir}/{chat_title_details}.json", "w", encoding="utf8") as file:
        json.dump(asdict(chat), file, sort_keys=True, indent=4, ensure_ascii=False)


def call_logs_to_json(call_log: CallLog, dir: str) -> None:
    """Store call logs as a JSON file.

    It takes a `CallLog` object and a directory path, and writes a JSON file to the directory with the
    name of the caller ID details

    Args:
        call_log (CallLog): CallLog - The call log object to be converted to JSON.
        dir (str): The directory where the JSON files will be saved.

    Returns:
        None: Creates .json file of the chat in the given directory
    """
    if call_log.caller_id.name and call_log.caller_id.number:
        caller_id_details = f"{call_log.caller_id.name} ({call_log.caller_id.number})"
    else:
        caller_id_details = f"+{call_log.caller_id.raw_string_jid.split('@')[0]}"

    with open(f"{dir}/{caller_id_details}.json", "w", encoding="utf8") as file:
        json.dump(asdict(call_log), file, sort_keys=True, indent=4, ensure_ascii=False)
