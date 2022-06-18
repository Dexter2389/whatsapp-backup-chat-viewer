import sqlite3

from src import resolver


def test_media_resolver():
    expected_results = [
        {
            "message_id": 158393,
            "media_job_uuid": "",
            "file_path": "",
            "mime_type": "video/mp4",
        },
        {
            "message_id": 158375,
            "media_job_uuid": "e16c9bec-0e8c-4beb-94bd-67ebb8103a64",
            "file_path": "Media/WhatsApp Images/IMG-20181127-WA0028.jpg",
            "mime_type": "image/jpeg",
        },
        {
            "message_id": 158357,
            "media_job_uuid": "692e849f-de91-4fdc-9962-c800ffa3f911",
            "file_path": "Media/WhatsApp Images/Sent/IMG-20181127-WA0026.jpg",
            "mime_type": "",
        },
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    message_ids = [158393, 158375, 158357]
    for message_id, expected_result in zip(message_ids, expected_results):
        assert resolver.media_resolver(msgdb_cursor, message_id) == expected_result

    msgdb.close()


def test_geo_position_resolver():
    expected_results = [
        {"message_id": 158394, "latitude": 65.754409, "longitude": -168.924534},
        None,
        {"message_id": 158397, "latitude": 55.84022, "longitude": -155.26259},
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    message_ids = [158394, 158375, 158397]
    for message_id, expected_result in zip(message_ids, expected_results):
        assert (
            resolver.geo_position_resolver(msgdb_cursor, message_id) == expected_result
        )

    msgdb.close()


def test_message_resolver():
    expected_results = [
        (
            {
                "message_id": 158393,
                "key_id": "3F78FF8EBE11E2EEC3DFD618AF3F9BBE",
                "chat_id": 463,
                "from_me": 0,
                "timestamp": 1543326217622,
                "text_data": "Nullam maximus est diam??",
                "reply_to": None,
            },
            "972071704671@s.whatsapp.net",
        ),
        (
            {
                "message_id": 158375,
                "key_id": "E00CEB0FF3CFCC183A2082D1478A3ACC",
                "chat_id": 545,
                "from_me": 0,
                "timestamp": 1543325180845,
                "text_data": "",
                "reply_to": None,
            },
            "589431685089@s.whatsapp.net",
        ),
        (
            {
                "message_id": 158357,
                "key_id": "C60A2E91152D8F72C84B2F3E3A509BB4",
                "chat_id": 533,
                "from_me": 1,
                "timestamp": 1543318731827,
                "text_data": "",
                "reply_to": None,
            },
            "997863428668@s.whatsapp.net",
        ),
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    message_ids = [158393, 158375, 158357]
    for message_id, expected_result in zip(message_ids, expected_results):
        assert resolver.message_resolver(msgdb_cursor, message_id) == expected_result

    msgdb.close()


def test_contact_resolver():
    expected_results = [
        {"name": "Tadgán Houtman", "number": "+972071704671"},
        {"name": "Vivamus bibendum", "number": ""},
        {"name": "Sung-Soo Kyler", "number": "+997863428668"},
    ]

    wadb = sqlite3.connect("tests/unit/data/test_wa.db")
    wadb_cursor = wadb.cursor()

    raw_string_jids = [
        "972071704671@s.whatsapp.net",
        "899167416177-1533072403@g.us",
        "997863428668@s.whatsapp.net",
    ]
    for raw_string_jid, expected_result in zip(raw_string_jids, expected_results):
        assert resolver.contact_resolver(wadb_cursor, raw_string_jid) == expected_result

    wadb.close()


def test_chat_resolver_with_ids():
    expected_results = [
        ({"chat_id": 463}, "972071704671@s.whatsapp.net"),
        ({"chat_id": 545}, "899167416177-1533072403@g.us"),
        ({"chat_id": 533}, "997863428668@s.whatsapp.net"),
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    chat_row_ids = [463, 545, 533]
    for chat_row_id, expected_result in zip(chat_row_ids, expected_results):
        assert (
            resolver.chat_resolver(msgdb_cursor, chat_row_id=chat_row_id)
            == expected_result
        )

    msgdb.close()


def test_chat_resolver_with_phone_number():
    expected_results = [
        ({"chat_id": 463}, "972071704671@s.whatsapp.net"),
        ({"chat_id": 545}, "899167416177-1533072403@g.us"),
        ({"chat_id": 533}, "997863428668@s.whatsapp.net"),
    ]

    msgdb = sqlite3.connect("tests/unit/data/test_msgstore.db")
    msgdb_cursor = msgdb.cursor()

    phone_numbers = ["972071704671", "899167416177-1533072403", "997863428668"]
    for phone_number, expected_result in zip(phone_numbers, expected_results):
        assert (
            resolver.chat_resolver(msgdb_cursor, phone_number=phone_number)
            == expected_result
        )

    msgdb.close()
