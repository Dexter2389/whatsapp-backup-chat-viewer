from datetime import datetime
from typing import List, Optional, Union

from attrs import define


@define
class ContactOrChatBase(object):
    raw_string_jid: str  # Who sent this message in a group message setting. Resolved from `message_view.sender_jid_row_id -> jid._id -> jid.raw_string`.


@define
class Contact(ContactOrChatBase):
    name: Optional[
        str
    ]  # Sender name. Resolved from `chat_view._id -> chat_view.raw_string_jid -> wa_contacts.jid -> wa_contacts.display_name` or `chat_view._id -> chat_view.raw_string_jid -> regex`.
    number: Optional[
        str
    ]  # Phone Number. Resolved from `chat_view._id -> chat_view.raw_string_jid -> wa_contacts.jid -> wa_contacts.number` or `chat_view._id -> chat_view.raw_string_jid -> regex`.


@define
class GroupName(ContactOrChatBase):
    name: Optional[
        str
    ]  # Group name. Resolved from `chat_view._id -> chat_view.raw_string_jid -> wa_contacts.jid -> wa_contacts.display_name` or `chat_view._id -> chat_view.raw_string_jid -> regex`.


@define
class Media(object):
    message_id: int  # Which message does this media belong to. Resolved from `message_media.message_row_id`.
    media_job_uuid: str  # Resolved from `message_media.media_job_uuid`.
    file_path: str  # Resolved from `message_media.file_path`.
    mime_type: str  # Resolved from `message_media.mime_type`.


@define
class Message(object):
    message_id: int  # Message ID. Resolved from `message_view._id`.
    key_id: str  # Key ID. Resolved from `message_view.key_id`.
    chat_id: str  # Which chat does this message belong to. Resolved from `message_view.chat_row_id`.
    from_me: int  # Whether this message is sent by me or not. Resolved from `message_view.from_me -> bool`.
    sender_contact: Optional[Contact]
    timestamp: datetime  # When was this message sent. Resolved from `message_view.received_timestamp`.
    text_data: Optional[
        str
    ]  # The actual text message. Resolved from `message_view.text_data`.
    media: Optional[Media]
    reply_to: str  # If a reply, it is a reply to which message. Resolved from `message_view._id -> message_quoted.message_row_id -> message_quoted.key_id`


@define
class Chat(object):
    chat_id: str  # Chat ID. Resolved from `chat_view._id`.
    chat_title: Optional[Union[Contact, GroupName]]  # Chat title.
    messages: List[Optional[Message]]
