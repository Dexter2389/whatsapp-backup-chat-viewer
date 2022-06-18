import sqlite3

from src.common import contact_resolver


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
        assert contact_resolver(wadb_cursor, raw_string_jid) == expected_result

    wadb.close()
