from typing import List, Optional, Union

from attrs import define


@define
class ContactOrChatBase(object):
    raw_string_jid: str  # Who sent this message in a group message setting. Resolved from `message.sender_jid_row_id -> jid._id -> jid.raw_string`.


@define
class Contact(ContactOrChatBase):
    name: Optional[
        str
    ]  # Sender name. Resolved from `chat._id -> chat.raw_string_jid -> wa_contacts.jid -> wa_contacts.display_name` or `chat._id -> chat.raw_string_jid -> regex`.
    number: Optional[
        str
    ]  # Phone Number. Resolved from `chat._id -> chat.raw_string_jid -> wa_contacts.jid -> wa_contacts.number` or `chat._id -> chat.raw_string_jid -> regex`.


@define
class GroupName(ContactOrChatBase):
    name: Optional[
        str
    ]  # Group name. Resolved from `chat._id -> chat.raw_string_jid -> wa_contacts.jid -> wa_contacts.display_name` or `chat._id -> chat.raw_string_jid -> regex`.


@define
class Media(object):
    message_id: int  # Which message does this media belong to. Resolved from `message_media.message_row_id`.
    media_job_uuid: str  # Resolved from `message_media.media_job_uuid`.
    file_path: str  # Resolved from `message_media.file_path`.
    mime_type: str  # Resolved from `message_media.mime_type`.


@define
class GeoPosition(object):
    message_id: int  # Which message does this media belong to. Resolved from `message_location.message_row_id`.
    latitude: float  # Resolved from `message_location.latitude`.
    longitude: float  # Resolved from `message_location.longitude`.


@define
class Message(object):
    message_id: int  # Message ID. Resolved from `message._id`.
    key_id: str  # Key ID. Resolved from `message.key_id`.
    chat_id: int  # Which chat does this message belong to. Resolved from `message.chat_row_id`.
    from_me: int  # Whether this message is sent by me or not. Resolved from `message.from_me -> bool`.
    sender_contact: Optional[Contact]
    timestamp: int  # When was this message sent. Resolved from `message.received_timestamp`.
    text_data: Optional[
        str
    ]  # The actual text message. Resolved from `message.text_data`.
    media: Optional[Media]
    geo_position: Optional[GeoPosition]
    reply_to: str| None  # If a reply, it is a reply to which message. Resolved from `message._id -> message_quoted.message_row_id -> message_quoted.key_id`


@define
class Chat(object):
    chat_id: int  # Chat ID. Resolved from `chat._id`.
    chat_title: Optional[Union[Contact, GroupName]]  # Chat title.
    messages: List[Optional[Message]]


@define
class Call(object):
    call_row_id: int  # Call row ID. Resolved from `call_log._id`.
    from_me: int  # Whether this call was made by me or not. Resolved from `call_log.from_me -> bool`.
    timestamp: int  # When was this call made. Resolved from `call_log.timestamp`.
    video_call: int  # Whether this call was a video call or not. Resolved from `call_log.video_call -> bool`.
    duration: int  # Duration of the call. Resolved from `call_log.duration`.
    call_result: int


@define
class CallLog(object):
    jid_row_id: int
    caller_id: Optional[Contact]
    calls: List[Optional[Call]]
