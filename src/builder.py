from itertools import chain

from .models import Media, Message, Chat, Contact, GroupName
from .resolver import chat_resolver, message_resolver, media_resolver, contact_resolver


def build_message_for_given_id(msgdb_cursor, wadb_cursor, message_id):
    message, raw_string_jid = message_resolver(
        msgdb_cursor=msgdb_cursor, message_row_id=message_id
    )

    if raw_string_jid:
        contact = contact_resolver(
            wadb_cursor=wadb_cursor, raw_string_jid=raw_string_jid
        )
        message["sender_contact"] = Contact(raw_string_jid=raw_string_jid, **contact)
    else:
        message["sender_contact"] = None

    media = media_resolver(msgdb_cursor=msgdb_cursor, message_row_id=message_id)
    if media:
        message["media"] = Media(**media)
    else:
        message["media"] = media

    return Message(**message)


def build_chat_for_given_id_or_phone_number(
    msgdb_cursor, wadb_cursor, chat_row_id=None, phone_number=None
):
    if chat_row_id:
        chat, raw_string_jid = chat_resolver(
            msgdb_cursor=msgdb_cursor, chat_row_id=chat_row_id
        )
    elif phone_number:
        chat, raw_string_jid = chat_resolver(
            msgdb_cursor=msgdb_cursor, phone_number=phone_number
        )
    else:
        raise Exception("'chat_row_id' and 'phone_number' both cannot be None")

    dm_or_group = contact_resolver(
        wadb_cursor=wadb_cursor, raw_string_jid=raw_string_jid
    )
    if dm_or_group.get("number"):
        chat["chat_title"] = Contact(raw_string_jid=raw_string_jid, **dm_or_group)
    else:
        chat["chat_title"] = GroupName(
            raw_string_jid=raw_string_jid, name=dm_or_group.get("name")
        )

    query = f"""SELECT message_view._id FROM 'message_view' WHERE message_view.chat_row_id={chat.get("chat_id")}"""
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None
    chat["messages"] = [
        build_message_for_given_id(msgdb_cursor, wadb_cursor, message_id)
        for message_id in res_query
    ]

    return Chat(**chat)


def build_all_chats(msgdb_cursor, wadb_cursor):
    query = f"""SELECT chat_view._id FROM 'chat_view'"""
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None
    chats = [
        build_chat_for_given_id_or_phone_number(
            msgdb_cursor=msgdb_cursor, wadb_cursor=wadb_cursor, chat_row_id=chat_id
        )
        for chat_id in res_query
    ]
    return chats
