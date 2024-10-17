import sqlite3
from itertools import chain
from typing import Generator, Union

from ..common import contact_resolver
from ..models import Call, CallLog, Contact
from .resolver import call_jid_resolver, call_resolver


def build_call_for_given_id(
    msgdb_cursor: sqlite3.Cursor, call_row_id: int
) -> Union[Call, None]:
    """Extract call details for a given call_row_id.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        call_row_id (int): ID of the call to extract.

    Returns:
        Call: Call details for the given call_row_id.
    """
    call_details = call_resolver(msgdb_cursor, call_row_id)

    if call_details:
        return Call(**call_details)
    else:
        return None


def build_call_log_for_given_id_or_phone_number(
    msgdb_cursor: sqlite3.Cursor,
    wadb_cursor: sqlite3.Cursor,
    jid_row_id: int = None,
    phone_number: str = None,
) -> Union[CallLog, None]:
    """Extract all call_logs (if available) for a given jid_row_id or phone_number.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        wadb_cursor (sqlite3.Cursor): 'wadb' cursor.
        jid_row_id (int, optional): jid of the call_log to extract. Defaults to None.
        phone_number (str, optional): Phone Number of the person you want to extract the call_logs of. Defaults to None.

    Returns:
        CallLog: CallLog object corresponding to the given jid_row_id or phone_number.
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
        raise AssertionError("'jid_row_id' and 'phone_number' cannot both be None")

    dm_or_group = contact_resolver(
        wadb_cursor=wadb_cursor, raw_string_jid=raw_string_jid
    )
    call_log["caller_id"] = Contact(raw_string_jid=raw_string_jid, **dm_or_group)

    query = f"""SELECT call_log._id FROM 'call_log' WHERE call_log.jid_row_id={call_log.get("jid_row_id")}"""
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))
    call_log["calls"] = [
        build_call_for_given_id(msgdb_cursor, call_row_id)
        for call_row_id in sorted(res_query)
    ]

    return CallLog(**call_log)


def build_all_call_logs(
    msgdb_cursor: sqlite3.Cursor, wadb_cursor: sqlite3.Cursor
) -> Generator[CallLog, None, None]:
    """Extract all call_logs in the msgdb database.

    Args:
        msgdb_cursor (sqlite3.Cursor): 'msgdb' cursor.
        wadb_cursor (sqlite3.Cursor): 'wadb' cursor.

    Returns:
        A generator of CallLog objects
    """
    query = "SELECT jid._id FROM 'jid'"
    exec = msgdb_cursor.execute(query)
    res_query = list(chain.from_iterable(exec.fetchall()))

    return (
        build_call_log_for_given_id_or_phone_number(
            msgdb_cursor=msgdb_cursor, wadb_cursor=wadb_cursor, jid_row_id=jid_row_id
        )
        for jid_row_id in sorted(res_query)
    )
