from typing import Optional, List
from datetime import datetime

from markdown import markdown
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

from ai import MODEL_TOKEN_LIMIT
from ai.tokens import token_count_single_message
from utils.regexp import replace_code_blocks, escape_lt_gt_inside_code_tags


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    conversation_id: Optional[int] = Field(
        default=None, foreign_key="conversations.id")
    conversations: Optional["Conversation"] = Relationship(
        back_populates="messages")

    def to_chatgpt(self):
        '''Converts a Message to a ChatGPT message.'''
        return {
            'role': self.role,
            'content': self.content,
        }

    def to_html(self):
        '''render markdown to html'''
        return {
            'role': self.role,
            # TODO fix later
            # this was written in 2023, comment what year it was when you found this
            'content': escape_lt_gt_inside_code_tags(markdown(replace_code_blocks(self.content)).replace('</p>', '</p><br/>').replace('<ol>', '<ol class="list-disc">')),
            'id': self.id,
        }

    @classmethod
    def from_chatgpt(role, content):
        return Message(
            role=role,
            content=content,
        )


class PartialFile(SQLModel, table=True):
    __tablename__ = "partial_files"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    content: str
    file_upload_id: Optional[int] = Field(
        default=None, foreign_key="file_uploads.id")
    embeddings: Optional[List[float]] = Field(
        default=None, sa_column=Column(JSON))
    file_uploads: Optional["FileUpload"] = Relationship(
        back_populates="parts")


class FileUpload(SQLModel, table=True):
    __tablename__ = "file_uploads"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    filename: str
    parts: Optional[List[PartialFile]] = Relationship(
        back_populates="file_uploads")
    conversation_id: Optional[int] = Field(
        default=None, foreign_key="conversations.id")
    conversations: Optional["Conversation"] = Relationship(
        back_populates="file_uploads")


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    title: str = Field(default="New Chat")
    file_uploads: Optional[List[FileUpload]] = Relationship(
        back_populates="conversations")
    messages: Optional[List[Message]] = Relationship(
        back_populates="conversations")

    def to_chatgpt(self, model="gpt-3.5"):
        '''Converts a Conversation to a ChatGPT conversation.'''
        token_limit = MODEL_TOKEN_LIMIT.get(model, 4096)
        messages = [{
            'role': 'system',
            'content': 'You are a helpful assistant.',
        }]
        if self.messages:
            # get messages in chatgpt format
            chatgpt_messages = [message.to_chatgpt()
                                for message in self.messages if message]
            # always make sure the newest message is first
            chatgpt_messages.reverse()
            # temp list to hold new messages
            new_message_list = []
            # get the token count of the first message
            token_count = token_count_single_message(messages[0], model)
            for message in chatgpt_messages:
                msg_tokens = token_count_single_message(message, model)
                if token_count + msg_tokens < token_limit:
                    new_message_list.append(message)
                    token_count += msg_tokens
            # add new message list, reversed, to the messages list
            new_message_list.reverse()
            messages += new_message_list

        return messages

    def to_html(self):
        '''Converts a conversation to html'''
        # render every message as html
        messages = [message.to_html() for message in self.messages if message]
        return messages
