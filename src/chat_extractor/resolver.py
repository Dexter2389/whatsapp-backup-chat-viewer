import sqlite3
from typing import Any, Dict, Tuple, Union


def media_resolver(msgdb_cursor: sqlite3.Cursor, message_row_id: int) -> Dict[str, Any] | None:
    """Fetch media related data for a given message_id from the msgdb.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        message_row_id (int): ID of the message for which media data is retrieved.

    Returns:
        Dict[str, Any]: Dictionary containing 'message_id', 'media_job_uuid', 'file_path' and 'mime_type' keys.
    """
    query = f"SELECT message_media.message_row_id as message_id, message_media.media_job_uuid, message_media.file_path, message_media.mime_type FROM message_media WHERE message_media.message_row_id='{message_row_id}'"
    exec = msgdb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    return res


def geo_position_resolver(
    msgdb_cursor: sqlite3.Cursor, message_row_id: int
) -> Dict[str, Any] | None:
    """Fetch geo-position related data for a given message_id from the msgdb.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        message_row_id (int): ID of the message for which media data is retrieved.

    Returns:
        Dict[str, Any]: Dictionary containing 'message_id', 'latitude' and 'longitude' keys.
    """
    query = f"SELECT message_location.message_row_id as message_id, message_location.latitude, message_location.longitude FROM message_location WHERE message_location.message_row_id='{message_row_id}'"
    exec = msgdb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    return res


def message_resolver(
    msgdb_cursor: sqlite3.Cursor, message_row_id: int
) -> Tuple[Dict[str, Any], str]:
    """Fetch message data for a given message_id from the msgdb.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        message_row_id (int): ID of the message for which message data is retrieved.

    Returns:
        Dict[str, Any]: Dictionary containing 'message_id', 'key_id', 'chat_id', 'from_me', 'raw_string_jid', 'timestamp', 'text_data' and 'message_quoted.key_id' keys.
        str: 'raw_string_jid' of the person who sent the message
    """
    query = f"""
    SELECT message._id as message_id, message.key_id, message.chat_row_id as chat_id, message.from_me, jid.raw_string as raw_string_jid, (CASE WHEN message.received_timestamp=0 THEN message.timestamp ELSE message.received_timestamp END) as timestamp, message.text_data, message_quoted.key_id as reply_to
    FROM 'message'
    LEFT JOIN 'message_quoted' ON message._id=message_quoted.message_row_id
    JOIN 'jid', 'chat' ON message.sender_jid_row_id=jid._id OR message.chat_row_id=chat._id AND chat.jid_row_id=jid._id
    WHERE message._id={message_row_id}
    """

    exec = msgdb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        res_query = [
            None,
            None,
        ]
    res = dict(zip([col[0] for col in exec.description], res_query))
    raw_string_jid = res.pop("raw_string_jid")
    return res, raw_string_jid


def chat_resolver(
    msgdb_cursor: sqlite3.Cursor,
    chat_row_id: Union[int, None] = None,
    phone_number: Union[str, None] = None,
) -> Tuple[Dict[str, Any], str]:
    """Fetch chat data for a given chat_row_id from the msgdb.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        chat_row_id (Union[int, None]): ID of the chat for which chat data is retrieved. Defaults to None.
        phone_number (Union[str, None]): Phone number of the chat for which chat data is retrieved. Defaults to None.

    Returns:
        Dict[str, Any]: Dictionary containing 'chat_id' as key.
        str: 'raw_string_jid' of the person who sent the message.
    """
    if chat_row_id:
        msgdb_query = f"""
        SELECT chat._id as chat_id, jid.raw_string as raw_string_jid
        FROM 'chat'
        JOIN 'jid' ON chat.jid_row_id=jid._id
        WHERE chat._id={chat_row_id}"""
    elif phone_number:
        msgdb_query = f"""
        SELECT chat._id as chat_id, jid.raw_string as raw_string_jid
        FROM 'chat'
        JOIN 'jid' ON chat.jid_row_id=jid._id
        WHERE jid.raw_string LIKE '%{phone_number}@%'"""
    else:
        raise AssertionError("'chat_row_id' and 'phone_number' both cannot be None")

    exec = msgdb_cursor.execute(msgdb_query)
    res_query = exec.fetchone()
    if res_query is None:
        res_query = [
            None,
            None,
        ]  # Need some better logic to resolve when we don't have a contact in msgdb.db
    res = dict(zip([col[0] for col in exec.description], res_query))
    raw_string_jid = res.pop("raw_string_jid")
    return res, raw_string_jid
