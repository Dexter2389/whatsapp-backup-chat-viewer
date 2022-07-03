import sqlite3
from itertools import chain
from typing import Generator, Union

from ..common import contact_resolver
from ..models import Chat, Contact, GeoPosition, GroupName, Media, Message
from .resolver import (
    chat_resolver,
    geo_position_resolver,
    media_resolver,
    message_resolver,
)


def build_message_for_given_id(
    msgdb_cursor: sqlite3.Cursor, wadb_cursor: sqlite3.Cursor, message_id: int
) -> Message:
    """Extract text message, media (if available) and location (if available) for a given message_id.

    It takes a message id, and returns a Message object

    Args:
        msgdb_cursor (sqlite3.Cursor): The cursor for the 'msgdb' database.
        wadb_cursor (sqlite3.Cursor): The cursor for the 'wadb.db' database.
        message_id (int): The message id of the message you want to extract.

    Returns:
        A Message object corresponding to the given message_id.
    """
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
        message["media"] = None

    geo_position = geo_position_resolver(
        msgdb_cursor=msgdb_cursor, message_row_id=message_id
    )
    if geo_position:
        message["geo_position"] = GeoPosition(**geo_position)
    else:
        message["geo_position"] = None

    return Message(**message)


def build_chat_for_given_id_or_phone_number(
    msgdb_cursor: sqlite3.Cursor,
    wadb_cursor: sqlite3.Cursor,
    chat_row_id: int = None,
    phone_number: str = None,
) -> Union[Chat, None]:
    """Extract all the messages and media (if available) for a given chat_row_id or phone_number.

    It takes a chat_row_id or phone_number and returns a Chat object.

    Args:
        msgdb_cursor (sqlite3.Cursor): The cursor for the 'msgdb' database.
        wadb_cursor (sqlite3.Cursor): The cursor for the 'wadb' database.
        chat_row_id (int): ID of the chat to extract. Defaults to None.
        phone_number (str): Phone Number of the person you want to extract the chats of. Defaults to None.

    Returns:
        Chat: Chat corresponding to the given chat_row_id or phone_number.
    """
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

    query = f"""SELECT message._id FROM 'message' WHERE message.chat_row_id={chat.get("chat_id")}"""
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None
    chat["messages"] = [
        build_message_for_given_id(msgdb_cursor, wadb_cursor, message_id)
        for message_id in res_query
    ]

    return Chat(**chat)


def build_all_chats(
    msgdb_cursor: sqlite3.Cursor, wadb_cursor: sqlite3.Cursor
) -> Generator[Chat, None, None]:
    """Extract all chats in the msgdb database.

    It takes a cursor to the message database and a cursor to the wa database, and returns a generator
    that yields a chat object for each chat in the message database.

    Args:
        msgdb_cursor (sqlite3.Cursor): The cursor for the 'msgdb' database.
        wadb_cursor (sqlite3.Cursor): The cursor for the 'wadb' database.

    Yields:
        A generator of Chat objects.
    """
    query = "SELECT chat._id FROM 'chat'"
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None

    for chat_id in res_query:
        yield build_chat_for_given_id_or_phone_number(
            msgdb_cursor=msgdb_cursor, wadb_cursor=wadb_cursor, chat_row_id=chat_id
        )
