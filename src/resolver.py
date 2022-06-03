def media_resolver(msgdb_cursor, message_row_id):
    query = f"SELECT message_media.message_row_id as message_id, message_media.media_job_uuid, message_media.file_path, message_media.mime_type FROM message_media WHERE message_media.message_row_id='{message_row_id}'"
    exec = msgdb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    return res


def message_resolver(msgdb_cursor, message_row_id):
    query = f"""
    SELECT message_view._id as message_id, message_view.key_id, message_view.chat_row_id as chat_id, message_view.from_me, (CASE WHEN jid.raw_string IS NULL THEN chat_view.raw_string_jid ELSE jid.raw_string END) as raw_string_jid, (CASE WHEN message_view.received_timestamp=0 THEN message_view.timestamp ELSE message_view.received_timestamp END) as timestamp, message_view.text_data, message_quoted.key_id as reply_to
    FROM 'message_view'
    LEFT JOIN 'message_quoted' ON message_view._id=message_quoted.message_row_id
    LEFT JOIN 'jid' ON message_view.sender_jid_row_id=jid._id
    JOIN 'chat_view' ON message_view.chat_row_id=chat_view._id
    WHERE message_view._id={message_row_id}
    """

    exec = msgdb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    raw_string_jid = res.pop("raw_string_jid")
    return res, raw_string_jid


def contact_resolver(wadb_cursor, raw_string_jid):
    query = f"""
    SELECT wa_contacts.display_name as name, wa_contacts.number FROM 'wa_contacts' WHERE wa_contacts.jid="{raw_string_jid}"
    """
    exec = wadb_cursor.execute(query)
    res_query = exec.fetchone()
    if res_query is None:
        res_query = [
            None,
            None,
        ]  # Need some better logic to resolve when we don't have a contact in wa.db
    res = dict(zip([col[0] for col in exec.description], res_query))
    return res


def chat_resolver(msgdb_cursor, chat_row_id=None, phone_number=None):
    if chat_row_id:
        msgdb_query = f"""SELECT chat_view._id as chat_id, chat_view.raw_string_jid FROM 'chat_view' WHERE chat_view._id={chat_row_id}"""
    elif phone_number:
        msgdb_query = f"""SELECT chat_view._id as chat_id, chat_view.raw_string_jid FROM 'chat_view' WHERE chat_view.raw_string_jid LIKE '%{phone_number}@%'"""
    else:
        raise Exception("'chat_row_id' and 'phone_number' both cannot be None")

    exec = msgdb_cursor.execute(msgdb_query)
    res_query = exec.fetchone()
    if res_query is None:
        return None
    res = dict(zip([col[0] for col in exec.description], res_query))
    raw_string_jid = res.pop("raw_string_jid")
    return res, raw_string_jid
