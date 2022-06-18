import sqlite3

from src.call_log_extractor import builder
from tests.unit.data.expected_call_log_builder_results import (
    expected_build_all_call_logs,
    expected_build_call_for_given_id_results,
    expected_build_call_log_for_given_id_or_phone_number_results,
)


def test_build_call_for_given_id():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    call_row_ids = [929, 2909, 8]
    for (call_row_id, expected_result) in zip(
        call_row_ids, expected_build_call_for_given_id_results
    ):
        assert (
            builder.build_call_for_given_id(msgdb_cursor, call_row_id)
            == expected_result
        )

    msgdb.close()


def test_build_call_log_for_given_id():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    jid_row_ids = [1, 179, 16]
    for (jid_row_id, expected_result) in zip(
        jid_row_ids, expected_build_call_log_for_given_id_or_phone_number_results
    ):
        assert (
            builder.build_call_log_for_given_id_or_phone_number(
                msgdb_cursor, wadb_cursor, jid_row_id=jid_row_id
            )
            == expected_result
        )

    msgdb.close()
    wadb.close()


def test_build_call_log_for_phone_number():
    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()
    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    phone_numbers = ["728678956227", "576697466685", "669233817152"]
    for (phone_number, expected_result) in zip(
        phone_numbers, expected_build_call_log_for_given_id_or_phone_number_results
    ):
        assert (
            builder.build_call_log_for_given_id_or_phone_number(
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

    assert (
        builder.build_all_call_logs(msgdb_cursor, wadb_cursor)
        == expected_build_all_call_logs
    )

    msgdb.close()
    wadb.close()
