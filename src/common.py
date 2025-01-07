import sqlite3
from typing import Any, Dict


def contact_resolver(
    wadb_cursor: sqlite3.Cursor, raw_string_jid: str
) -> Dict[str, Any]:
    """Fetch contact data for a given raw_string_jid from the wadb.

    Args:
        wadb_cursor (sqlite3.Cursor): 'wadb' cursor
        raw_string_jid (str): JID of the person who for which contact data is retrieved

    Returns:
        Dict[str, Any]: Dictionary containing 'name' and 'number' keys.
    """
    query = f"""
    SELECT wa_contacts.display_name as name, wa_contacts.number FROM 'wa_contacts' WHERE wa_contacts.jid="{raw_string_jid}"
    """
    execution = wadb_cursor.execute(query)
    res_query = execution.fetchone()
    if res_query is None:
        res_query = [
            None,
            None,
        ]  # Need some better logic to resolve when we don't have a contact in wa.db
    res = dict(zip([col[0] for col in execution.description], res_query))
    if res.get("name"):
        if "/" in res["name"]:
            res["name"] = res.get("name").replace("/", "_")
    return res
