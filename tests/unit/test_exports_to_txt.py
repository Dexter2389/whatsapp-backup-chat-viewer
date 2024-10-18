from src.exports import to_txt
from src.models import (
    Call,
    CallLog,
    Chat,
    Contact,
    GeoPosition,
    GroupName,
    Media,
    Message,
)

from .data.expected_export_to_txt_results import (
    expected_export_call_logs_to_txt_formatted_result,
    expected_export_call_logs_to_txt_raw_result,
    expected_export_chats_to_txt_formatted_result,
    expected_export_chats_to_txt_raw_result,
)


def test_export_chats_to_txt_raw(tmp_path):
    test_chat = Chat(
        chat_id=533,
        chat_title=Contact(
            raw_string_jid="997863428668@s.whatsapp.net",
            name="Sung-Soo Kyler",
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
                    name="Sung-Soo Kyler",
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
                    name="Sung-Soo Kyler",
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
                    name="Sung-Soo Kyler",
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

    to_txt.chats_to_txt_raw(chat=test_chat, folder=f"{test_chat_dir}")
    with open(
        f"{test_chat_dir}/{test_chat.chat_title.name} ({test_chat.chat_title.number})-raw.txt"
    ) as f:
        assert f.read() == expected_export_chats_to_txt_raw_result


def test_export_chats_to_txt_formatted(tmp_path):
    test_chat = Chat(
        chat_id=533,
        chat_title=GroupName(
            raw_string_jid="899167416177-1533072403@g.us", name="Vivamus bibendum"
        ),
        messages=[
            Message(
                message_id=158352,
                key_id="6BE2CB39DE7CE864C49F28F6B11EAD05",
                chat_id=533,
                from_me=1,
                sender_contact=Contact(
                    raw_string_jid="997863428668@s.whatsapp.net",
                    name="Sung-Soo Kyler",
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
                    name="Sung-Soo Kyler",
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
                    name="Sung-Soo Kyler",
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
    to_txt.chats_to_txt_formatted(chat=test_chat, folder=f"{test_chat_dir}")
    with open(f"{test_chat_dir}/{test_chat.chat_title.name}.txt") as f:
        assert f.read() == expected_export_chats_to_txt_formatted_result


def test_export_call_logs_to_txt_raw(tmp_path):
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
                from_me=1,
                timestamp=1568973142212,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            None,
        ],
    )

    test_call_log_dir = tmp_path / "call_logs"
    test_call_log_dir.mkdir()
    to_txt.call_logs_to_txt_raw(call_log=test_call_log, folder=f"{test_call_log_dir}")
    with open(
        f"{test_call_log_dir}/{test_call_log.caller_id.name} ({test_call_log.caller_id.number})-raw.txt"
    ) as f:
        assert f.read() == expected_export_call_logs_to_txt_raw_result


def test_export_call_logs_to_txt_formatted(tmp_path):
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
    to_txt.call_logs_to_txt_formatted(
        call_log=test_call_log, folder=f"{test_call_log_dir}"
    )
    with open(
        f"{test_call_log_dir}/{test_call_log.caller_id.name} ({test_call_log.caller_id.number}).txt"
    ) as f:
        assert f.read() == expected_export_call_logs_to_txt_formatted_result
