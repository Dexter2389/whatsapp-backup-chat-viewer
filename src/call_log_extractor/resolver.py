import sqlite3
from typing import Any, Dict, Tuple, Union


def call_resolver(msgdb_cursor: sqlite3.Cursor, call_row_id: int) -> Dict[str, Any]:
    """Fetch call data for a given call_row_id from the msgdb.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        call_row_id (int): ID of the row for which call data is retrieved.

    Returns:
        Dict[str, Any]: Dictionary containing 'call_row_id', 'from_me', 'timestamp', 'video_call', 'duration' and 'call_result' keys.
    """
    msgdb_query = f"""
    SELECT call_log._id as call_row_id, call_log.from_me, call_log.timestamp, call_log.video_call, call_log.duration, call_log.call_result
    FROM 'call_log'
    WHERE call_log._id={call_row_id}"""
    exec = msgdb_cursor.execute(msgdb_query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    return res


def call_jid_resolver(
    msgdb_cursor: sqlite3.Cursor,
    jid_row_id: Union[int, None] = None,
    phone_number: Union[str, None] = None,
) -> Tuple[Dict[str, Any], str]:
    """Fetch jid data for a given jid_row_id from the msgdb for fetching call logs.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        jid_row_id (Union[int, None]): jid_row of the caller for which call data is retrieved. Defaults to None.
        phone_number (Union[str, None]): Phone number of the caller for which call data is retrieved. Defaults to None.

    Returns:
        Dict[str, Any]: Dictionary containing 'jid_row_id' as key.
        str: 'raw_string_jid' of the person who sent the message.
    """
    if jid_row_id:
        msgdb_query = f"""
        SELECT jid._id as jid_row_id, jid.raw_string as raw_string_jid
        FROM 'jid'
        WHERE jid._id={jid_row_id}"""
    elif phone_number:
        msgdb_query = f"""
        SELECT jid._id as jid_row_id, jid.raw_string as raw_string_jid
        FROM 'jid'
        WHERE jid.raw_string LIKE '%{phone_number}@%'"""
    else:
        raise Exception("'jid_row_id' and 'phone_number' both cannot be None")

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
