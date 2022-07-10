import json

from deepdiff import DeepDiff

from src.exports import to_json
from src.models import Call, CallLog, Chat, Contact, GeoPosition, Media, Message


def test_export_chats_to_json(tmp_path):
    test_chat = Chat(
        chat_id=533,
        chat_title=Contact(
            raw_string_jid="997863428668@s.whatsapp.net",
            name=None,
            number="+997863428668",
        ),
        messages=[
            Message(
                message_id=158352,
                key_id="6BE2CB39DE7CE864C49F28F6B11EAD05",
                chat_id=533,
                from_me=1,
                sender_contact=Contact(
                    raw_string_jid="997863428668@s.whatsapp.net",
                    name=None,
                    number="+997863428668",
                ),
                timestamp=1543317689901,
                text_data="Nulla scelerisque leo augue, sit amet ullamcorper est aliquet sed!! 😂",
                media=Media(
                    message_id=158352,
                    media_job_uuid="fbc84a18-aacf-4bbe-a736-a968e5ca82e5",
                    file_path="Media/WhatsApp Images/Sent/IMG-20181127-WA0025.jpg",
                    mime_type="",
                ),
                geo_position=None,
                reply_to=None,
            ),
            Message(
                message_id=158353,
                key_id="FBCEBE15C475DCE9F74087D8735CABB0",
                chat_id=533,
                from_me=1,
                sender_contact=Contact(
                    raw_string_jid="997863428668@s.whatsapp.net",
                    name=None,
                    number="+997863428668",
                ),
                timestamp=1543317698865,
                text_data="Fusce mollis libero!!",
                media=None,
                geo_position=None,
                reply_to=None,
            ),
            Message(
                message_id=158394,
                key_id="3D15299A2A6B62DBC5BEC42E42C9E48A",
                chat_id=456,
                from_me=1,
                sender_contact=Contact(
                    raw_string_jid="997863428668@s.whatsapp.net",
                    name=None,
                    number="+997863428668",
                ),
                timestamp=1580132486421,
                text_data="",
                media=None,
                geo_position=GeoPosition(
                    message_id=158394, latitude=65.754409, longitude=-168.924534
                ),
                reply_to="6BE2CB39DE7CE864C49F28F6B11EAD05",
            ),
        ],
    )

    test_chat_dir = tmp_path / "chats"
    test_chat_dir.mkdir()
    to_json.chats_to_json(chat=test_chat, dir=f"{test_chat_dir}")

    with open(
        f"{test_chat_dir}/+{test_chat.chat_title.raw_string_jid.split('@')[0]}.json",
        encoding="utf8",
    ) as f:
        chat_json = json.load(f)

    with open(
        "tests/unit/data/expected_export_to_json_chat.json",
        encoding="utf8",
    ) as f:
        expected_result = json.load(f)

    assert (
        DeepDiff(chat_json, expected_result, ignore_order=True, report_repetition=True)
        == {}
    )


def test_export_call_logs_to_json(tmp_path):
    test_call_log = CallLog(
        jid_row_id=16,
        caller_id=Contact(
            raw_string_jid="669233817152@s.whatsapp.net",
            name="Izebel Bengtsdotter",
            number="+669233817152",
        ),
        calls=[
            Call(
                call_row_id=929,
                from_me=1,
                timestamp=1545829680246,
                video_call=0,
                duration=0,
                call_result=4,
            ),
            Call(
                call_row_id=2909,
                from_me=0,
                timestamp=1568973142212,
                video_call=0,
                duration=72,
                call_result=2,
            ),
            None,
        ],
    )

    test_call_log_dir = tmp_path / "call_logs"
    test_call_log_dir.mkdir()
    to_json.call_logs_to_json(call_log=test_call_log, dir=f"{test_call_log_dir}")

    with open(
        f"{test_call_log_dir}/{test_call_log.caller_id.name} ({test_call_log.caller_id.number}).json",
        encoding="utf8",
    ) as f:
        call_log_json = json.load(f)

    with open(
        "tests/unit/data/expected_export_to_json_call_log.json",
        encoding="utf8",
    ) as f:
        expected_result = json.load(f)

    assert (
        DeepDiff(
            call_log_json, expected_result, ignore_order=True, report_repetition=True
        )
        == {}
    )
