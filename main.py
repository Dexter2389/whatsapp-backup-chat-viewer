import argparse
import sqlite3
from typing import List, Tuple

from src import builder
from src.exports.to_txt import chats_to_txt_formatted, chats_to_txt_raw


def create_db_connection(file_path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db = sqlite3.connect(file_path)
    return db, db.cursor()


def close_db_connections(databases: List[sqlite3.Connection]) -> None:
    for db in databases:
        db.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Project to extract Whatsapp conversations from the app's SQLite database and exporting them as JSON or TXT files."
    )
    ap.add_argument(
        "--msgdb", "-mdb", type=str, required=True, help="Path to 'msgstore.db' file"
    )
    ap.add_argument(
        "--wadb", "-wdb", type=str, required=True, help="Path to 'wa.db' file"
    )
    ap.add_argument(
        "--chat_output_style",
        "-f",
        choices=["raw_txt", "formatted_txt", "json"],
        type=str,
        default="formatted",
        help="Style in which your parsed messages will be stored",
    )
    ap.add_argument(
        "--parsed_chat_output_dir",
        "-o",
        type=str,
        help="Path to directory where your parsed chats will be stored",
    )
    ap.add_argument(
        "--extract_chat",
        "-e",
        nargs="*",
        default="all",
        help="Phone numbers of the chats that you want to extract from the database",
    )
    args = ap.parse_args()

    msgdb, msgdb_cursor = create_db_connection(args.msgdb)
    wadb, wadb_cursor = create_db_connection(args.wadb)

    if args.chat_output_style == "raw":
        if args.extract_chat == "all":
            chats = builder.build_all_chats(msgdb_cursor, wadb_cursor)
            for chat in chats:
                chats_to_txt_raw(
                    chat=chat,
                    dir=args.parsed_chat_output_dir,
                )
        else:
            for ph_no in args.extract_chat:
                chat = builder.build_chat_for_given_id_or_phone_number(
                    msgdb_cursor, wadb_cursor, phone_number=ph_no
                )
                chats_to_txt_raw(
                    chat=chat,
                    dir=args.parsed_chat_output_dir,
                )
    elif args.chat_output_style == "formatted":
        if args.extract_chat == "all":
            chats = builder.build_all_chats(msgdb_cursor, wadb_cursor)
            for chat in chats:
                chats_to_txt_formatted(
                    chat=chat,
                    dir=args.parsed_chat_output_dir,
                )
        else:
            for ph_no in args.extract_chat:
                chat = builder.build_chat_for_given_id_or_phone_number(
                    msgdb_cursor, wadb_cursor, phone_number=ph_no
                )
                chats_to_txt_formatted(
                    chat=chat,
                    dir=args.parsed_chat_output_dir,
                )
    elif args.chat_output_style == "json":
        close_db_connections([msgdb, wadb])
        raise NotImplementedError
    else:
        close_db_connections([msgdb, wadb])
        raise Exception("Invalid 'chat formatting' requested")

    close_db_connections([msgdb, wadb])
