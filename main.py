import argparse
import os
import sqlite3
from typing import List, Tuple

from tqdm import tqdm

from src.call_log_extractor import builder as call_log_builder
from src.chat_extractor import builder as chat_builder
from src.exports.to_json import call_logs_to_json, chats_to_json
from src.exports.to_txt import (
    call_logs_to_txt_formatted,
    call_logs_to_txt_raw,
    chats_to_txt_formatted,
    chats_to_txt_raw,
)

CALL_LOGS_DIR = "/call_logs"
CHAT_DIR = "/chats"


def create_db_connection(file_path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Create a database connection and return it.

    The function takes a single argument, `file_path`, which is a string. The function returns a tuple
    of two items: a `sqlite3.Connection` object and a `sqlite3.Cursor` object

    Args:
      file_path (str): The path to the database file.

    Returns:
      A tuple of the connection and cursor objects.
    """
    db = sqlite3.connect(file_path)
    return db, db.cursor()


def close_db_connections(databases: List[sqlite3.Connection]) -> None:
    """Close all the database connections in the list of database connections.

    The function takes a list of database connections and closes them all.

    Args:
      databases (List[sqlite3.Connection]): A list of sqlite3.Connection objects.
    """
    for db in databases:
        db.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Project to extract Whatsapp conversations and/or call logs from the app's SQLite database and exporting them as JSON or TXT files."
    )
    ap.add_argument(
        "--msgdb", "-mdb", type=str, required=True, help="Path to 'msgstore.db' file"
    )
    ap.add_argument(
        "--wadb", "-wdb", type=str, required=True, help="Path to 'wa.db' file"
    )
    ap.add_argument(
        "--backup_strategy",
        "-b",
        choices=["chats", "call_logs", "both"],
        type=str,
        default="both",
        help="Backup only chats, only call_logs or both",
    )
    ap.add_argument(
        "--backup_output_style",
        "-f",
        choices=["raw_txt", "formatted_txt", "json"],
        type=str,
        default="formatted_txt",
        help="Style in which your parsed backup will be stored",
    )
    ap.add_argument(
        "--parsed_backup_output_dir",
        "-o",
        type=str,
        help="Path to directory where your parsed chats and/or parsed call logs will be stored",
    )
    ap.add_argument(
        "--backup_specific_or_all_chat_call",
        "-e",
        nargs="*",
        default=["all"],
        help="Phone numbers (format: XXXXXXXXXXXX) of the chats and/or call logs that you want to extract from the database",
    )
    args = ap.parse_args()

    msgdb, msgdb_cursor = create_db_connection(args.msgdb)
    wadb, wadb_cursor = create_db_connection(args.wadb)

    args.backup_strategy = (
        ["chats", "call_logs"]
        if args.backup_strategy == "both"
        else [args.backup_strategy]
    )

    if args.backup_output_style == "raw_txt":
        if args.backup_specific_or_all_chat_call == ["all"]:
            if "chats" in args.backup_strategy:
                output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                if not os.path.exists(output_chat_directory):
                    os.makedirs(output_chat_directory)
                chats = chat_builder.build_all_chats(msgdb_cursor, wadb_cursor)
                for chat in tqdm(chats):
                    chats_to_txt_raw(
                        chat=chat,
                        folder=output_chat_directory,
                    )
            if "call_logs" in args.backup_strategy:
                output_call_logs_directory = (
                        args.parsed_backup_output_dir + CALL_LOGS_DIR
                )
                if not os.path.exists(output_call_logs_directory):
                    os.makedirs(output_call_logs_directory)
                call_logs = call_log_builder.build_all_call_logs(
                    msgdb_cursor, wadb_cursor
                )
                for call_log in tqdm(call_logs):
                    if call_log.calls:
                        call_logs_to_txt_raw(
                            call_log=call_log, folder=output_call_logs_directory
                        )
        else:
            for ph_no in tqdm(args.backup_specific_or_all_chat_call):
                if "chats" in args.backup_strategy:
                    output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                    if not os.path.exists(output_chat_directory):
                        os.makedirs(output_chat_directory)
                    chat = chat_builder.build_chat_for_given_id_or_phone_number(
                        msgdb_cursor, wadb_cursor, phone_number=ph_no
                    )
                    chats_to_txt_raw(
                        chat=chat,
                        folder=output_chat_directory,
                    )
                if "call_logs" in args.backup_strategy:
                    output_call_logs_directory = (
                            args.parsed_backup_output_dir + CALL_LOGS_DIR
                    )
                    if not os.path.exists(output_call_logs_directory):
                        os.makedirs(output_call_logs_directory)
                    call_log = (
                        call_log_builder.build_call_log_for_given_id_or_phone_number(
                            msgdb_cursor, wadb_cursor, phone_number=ph_no
                        )
                    )
                    if call_log.calls:
                        call_logs_to_txt_raw(
                            call_log=call_log, folder=output_call_logs_directory
                        )

    elif args.backup_output_style == "formatted_txt":
        if args.backup_specific_or_all_chat_call == ["all"]:
            if "chats" in args.backup_strategy:
                output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                if not os.path.exists(output_chat_directory):
                    os.makedirs(output_chat_directory)
                chats = chat_builder.build_all_chats(msgdb_cursor, wadb_cursor)
                for chat in tqdm(chats):
                    chats_to_txt_formatted(
                        chat=chat,
                        folder=output_chat_directory,
                    )
            if "call_logs" in args.backup_strategy:
                output_call_logs_directory = (
                        args.parsed_backup_output_dir + CALL_LOGS_DIR
                )
                if not os.path.exists(output_call_logs_directory):
                    os.makedirs(output_call_logs_directory)
                call_logs = call_log_builder.build_all_call_logs(
                    msgdb_cursor, wadb_cursor
                )
                for call_log in tqdm(call_logs):
                    if call_log.calls:
                        call_logs_to_txt_formatted(
                            call_log=call_log, folder=output_call_logs_directory
                        )
        else:
            for ph_no in tqdm(args.backup_specific_or_all_chat_call):
                if "chats" in args.backup_strategy:
                    output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                    if not os.path.exists(output_chat_directory):
                        os.makedirs(output_chat_directory)
                    chat = chat_builder.build_chat_for_given_id_or_phone_number(
                        msgdb_cursor, wadb_cursor, phone_number=ph_no
                    )
                    chats_to_txt_formatted(
                        chat=chat,
                        folder=output_chat_directory,
                    )
                if "call_logs" in args.backup_strategy:
                    output_call_logs_directory = (
                            args.parsed_backup_output_dir + CALL_LOGS_DIR
                    )
                    if not os.path.exists(output_call_logs_directory):
                        os.makedirs(output_call_logs_directory)
                    call_log = (
                        call_log_builder.build_call_log_for_given_id_or_phone_number(
                            msgdb_cursor, wadb_cursor, phone_number=ph_no
                        )
                    )
                    if call_log.calls:
                        call_logs_to_txt_formatted(
                            call_log=call_log, folder=output_call_logs_directory
                        )

    elif args.backup_output_style == "json":
        if args.backup_specific_or_all_chat_call == ["all"]:
            if "chats" in args.backup_strategy:
                output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                if not os.path.exists(output_chat_directory):
                    os.makedirs(output_chat_directory)
                chats = chat_builder.build_all_chats(msgdb_cursor, wadb_cursor)
                for chat in tqdm(chats):
                    chats_to_json(
                        chat=chat,
                        folder=output_chat_directory,
                    )
            if "call_logs" in args.backup_strategy:
                output_call_logs_directory = (
                        args.parsed_backup_output_dir + CALL_LOGS_DIR
                )
                if not os.path.exists(output_call_logs_directory):
                    os.makedirs(output_call_logs_directory)
                call_logs = call_log_builder.build_all_call_logs(
                    msgdb_cursor, wadb_cursor
                )
                for call_log in tqdm(call_logs):
                    if call_log.calls:
                        call_logs_to_json(
                            call_log=call_log, folder=output_call_logs_directory
                        )
        else:
            for ph_no in tqdm(args.backup_specific_or_all_chat_call):
                if "chats" in args.backup_strategy:
                    output_chat_directory = args.parsed_backup_output_dir + CHAT_DIR
                    if not os.path.exists(output_chat_directory):
                        os.makedirs(output_chat_directory)
                    chat = chat_builder.build_chat_for_given_id_or_phone_number(
                        msgdb_cursor, wadb_cursor, phone_number=ph_no
                    )
                    chats_to_json(
                        chat=chat,
                        folder=output_chat_directory,
                    )
                if "call_logs" in args.backup_strategy:
                    output_call_logs_directory = (
                            args.parsed_backup_output_dir + CALL_LOGS_DIR
                    )
                    if not os.path.exists(output_call_logs_directory):
                        os.makedirs(output_call_logs_directory)
                    call_log = (
                        call_log_builder.build_call_log_for_given_id_or_phone_number(
                            msgdb_cursor, wadb_cursor, phone_number=ph_no
                        )
                    )
                    if call_log.calls:
                        call_logs_to_json(
                            call_log=call_log, folder=output_call_logs_directory
                        )

    else:
        close_db_connections([msgdb, wadb])
        raise AssertionError("Invalid 'chat formatting' requested")

    close_db_connections([msgdb, wadb])
