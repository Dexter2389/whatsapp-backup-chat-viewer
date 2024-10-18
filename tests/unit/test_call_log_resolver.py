import sqlite3

from src.call_log_extractor import resolver


def test_call_resolver():
    expected_results = [
        {
            "call_row_id": 4001,
            "from_me": 1,
            "timestamp": 1578931156601,
            "video_call": 0,
            "duration": 5525,
            "call_result": 5,
        },
        {
            "call_row_id": 2342,
            "from_me": 1,
            "timestamp": 1565016395279,
            "video_call": 0,
            "duration": 0,
            "call_result": 2,
        },
        {
            "call_row_id": 8042,
            "from_me": 0,
            "timestamp": 1611287782000,
            "video_call": 1,
            "duration": 0,
            "call_result": 2,
        },
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    call_row_ids = [4001, 2342, 8042]
    for call_row_id, expected_result in zip(call_row_ids, expected_results):
        assert resolver.call_resolver(msgdb_cursor, call_row_id) == expected_result

    msgdb.close()


def test_call_jid_resolver_with_ids():
    expected_results = [
        ({"jid_row_id": 36}, "979017585714@s.whatsapp.net"),
        ({"jid_row_id": 26}, "899167416177@s.whatsapp.net"),
        ({"jid_row_id": 155}, "885402477365@s.whatsapp.net"),
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    jid_row_ids = [36, 26, 155]
    for jid_row_id, expected_result in zip(jid_row_ids, expected_results):
        assert (
            resolver.call_jid_resolver(msgdb_cursor, jid_row_id=jid_row_id)
            == expected_result
        )

    msgdb.close()


def test_call_jid_resolver_with_phone_number():
    expected_results = [
        ({"jid_row_id": 36}, "979017585714@s.whatsapp.net"),
        ({"jid_row_id": 26}, "899167416177@s.whatsapp.net"),
        ({"jid_row_id": 155}, "885402477365@s.whatsapp.net"),
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    phone_numbers = ["979017585714", "899167416177", "885402477365"]
    for phone_number, expected_result in zip(phone_numbers, expected_results):
        assert (
            resolver.call_jid_resolver(msgdb_cursor, phone_number=phone_number)
            == expected_result
        )

    msgdb.close()
