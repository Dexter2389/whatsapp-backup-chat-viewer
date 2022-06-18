import sqlite3
from itertools import chain
from typing import List, Union

from ..common import contact_resolver
from ..models import Call, CallLog, Contact
from .resolver import call_jid_resolver, call_resolver


def build_call_for_given_id(
    msgdb_cursor: sqlite3.Cursor, call_row_id: int
) -> Union[Call, None]:
    """_summary_

    Args:
        msgdb_cursor (sqlite3.Cursor): _description_
        call_row_id (int): _description_

    Returns:
        Call: _description_
    """
    call_details = call_resolver(msgdb_cursor, call_row_id)

    if call_details:
        return Call(**call_details)
    else:
        None


def build_call_log_for_given_id_or_phone_number(
    msgdb_cursor: sqlite3.Cursor,
    wadb_cursor: sqlite3.Cursor,
    jid_row_id: int = None,
    phone_number: str = None,
) -> Union[CallLog, None]:
    """_summary_

    Args:
        msgdb_cursor (sqlite3.Cursor): _description_
        wadb_cursor (sqlite3.Cursor): _description_
        jid_row_id (int, optional): _description_. Defaults to None.
        phone_number (str, optional): _description_. Defaults to None.

    Raises:
        Exception: _description_
    """
    if jid_row_id:
        call_log, raw_string_jid = call_jid_resolver(
            msgdb_cursor=msgdb_cursor, jid_row_id=jid_row_id
        )
    elif phone_number:
        call_log, raw_string_jid = call_jid_resolver(
            msgdb_cursor=msgdb_cursor, phone_number=phone_number
        )
    else:
        raise Exception("'jid_row_id' and 'phone_number' both cannot be None")

    dm_or_group = contact_resolver(
        wadb_cursor=wadb_cursor, raw_string_jid=raw_string_jid
    )
    call_log["caller_id"] = Contact(raw_string_jid=raw_string_jid, **dm_or_group)

    query = f"""SELECT call_log._id FROM 'call_log' WHERE call_log.jid_row_id={call_log.get("jid_row_id")}"""
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None
    call_log["calls"] = [
        build_call_for_given_id(msgdb_cursor, call_row_id)
        for call_row_id in sorted(res_query)
    ]

    return CallLog(**call_log)


def build_all_call_logs(
    msgdb_cursor: sqlite3.Cursor, wadb_cursor: sqlite3.Cursor
) -> List[CallLog]:
    """_summary_

    Args:
        msgdb_cursor (sqlite3.Cursor): _description_
        wadb_cursor (sqlite3.Cursor): _description_

    Returns:
        List[CallLog]: _description_
    """
    query = "SELECT jid._id FROM 'jid'"
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    if res_query is None:
        return None
    call_logs = []
    for jid_row_id in sorted(res_query):
        call_log = build_call_log_for_given_id_or_phone_number(
            msgdb_cursor=msgdb_cursor, wadb_cursor=wadb_cursor, jid_row_id=jid_row_id
        )
        if call_log.calls:
            call_logs.append(call_log)
    return call_logs
