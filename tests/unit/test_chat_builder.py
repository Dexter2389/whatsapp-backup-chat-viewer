import sqlite3

from src.chat_extractor import builder
from tests.unit.data.expected_chat_builder_results import (
    expected_build_all_chats,
    expected_build_chat_for_given_id_or_phone_number_results,
    expected_build_message_for_given_id_results,
)


def test_build_message_for_given_id():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    message_ids = [158393, 158375, 158357]
    for (message_id, expected_result) in zip(
        message_ids, expected_build_message_for_given_id_results
    ):
        assert (
            builder.build_message_for_given_id(msgdb_cursor, wadb_cursor, message_id)
            == expected_result
        )

    msgdb.close()
    wadb.close()


def test_build_chat_for_given_id():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    chat_row_ids = [463, 545, 533]
    for (chat_row_id, expected_result) in zip(
        chat_row_ids, expected_build_chat_for_given_id_or_phone_number_results
    ):
        assert (
            builder.build_chat_for_given_id_or_phone_number(
                msgdb_cursor, wadb_cursor, chat_row_id=chat_row_id
            )
            == expected_result
        )

    msgdb.close()
    wadb.close()


def test_build_chat_for_phone_number():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    phone_numbers = ["972071704671", "899167416177-1533072403", "997863428668"]
    for (phone_number, expected_result) in zip(
        phone_numbers, expected_build_chat_for_given_id_or_phone_number_results
    ):
        assert (
            builder.build_chat_for_given_id_or_phone_number(
                msgdb_cursor, wadb_cursor, phone_number=phone_number
            )
            == expected_result
        )

    msgdb.close()
    wadb.close()


def test_build_all_chats():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    assert [
        chat for chat in builder.build_all_chats(msgdb_cursor, wadb_cursor)
    ] == expected_build_all_chats

    msgdb.close()
    wadb.close()
