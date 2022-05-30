import sqlite3
from src import resolver, builder
from src.export_to_txt import chats_to_txt_raw, chats_to_txt_formatted

msgdb = sqlite3.connect("msgstore.db")
msgdb_cursor = msgdb.cursor()


wadb = sqlite3.connect("wa.db")
wadb_cursor = wadb.cursor()

chats_to_txt_formatted(
    builder.build_chat_for_given_id(msgdb_cursor, wadb_cursor, 469), "output"
)

msgdb.close()
wadb.close()
