import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
import openai

from db import new_engine, Message, Conversation

load_dotenv()

MODEL = 'gpt-3.5-turbo'

openai.api_key = os.getenv('OPENAI_API_KEY')

engine = new_engine()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def root():
    # create a new conversation
    with Session(engine) as session:
        conversation = Conversation()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return RedirectResponse(url=f"/conversation/{conversation.id}", status_code=302)


@app.get('/conversation/{convo_id}')
async def get_conversation(convo_id: int, request: Request):
    with Session(engine) as session:
        statement = select(Conversation).where(Conversation.id == convo_id)
        conversation: Conversation = session.exec(statement).first()
        statement = select(Conversation)
        conversations = session.exec(statement).all()
        conversations.reverse()
        return templates.TemplateResponse("index.html", {"request": request, "title": conversation.title, "convo_id": convo_id, "convos": conversations, "messages": conversation.to_html()})


@app.delete('/conversation/{convo_id}')
async def delete_conversation(convo_id: int):
    with Session(engine) as session:
        conversation = session.get(Conversation, convo_id)
        session.delete(conversation)
        session.commit()
        return Response(status_code=200, content="", media_type="text/plain")


@app.post('/conversation')
async def create_conversation(conversation: Conversation):
    with Session(engine) as session:
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation


@app.patch('/conversation/{convo_id}/title')
async def update_conversation_title(request: Request, convo_id: int, title: Annotated[str, Form()]):
    with Session(engine) as session:
        statement = select(Conversation).where(Conversation.id == convo_id)
        conversation: Conversation = session.exec(statement).first()
        conversation.title = title
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return Response(status_code=200, content=conversation.title, media_type="text/plain")


@app.post('/conversation/{convo_id}/send')
async def send_message(message: Message, convo_id: int):
    '''Sends a message and responds with complete conversation'''
    with Session(engine) as session:
        # get the entire message history
        statement = select(Conversation).where(Conversation.id == convo_id)
        conversation: Conversation = session.exec(statement).first()
        # add the new message to the conversation
        message.conversation_id = convo_id
        session.add(message)
        session.commit()
        session.refresh(message)
        # send the message to OpenAI
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=conversation.to_chatgpt()
        )
        response_message = response.choices[0].message
        new_message = Message(
            role=response_message['role'],
            content=response_message['content'],
            conversation_id=convo_id
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        # return the entire conversation
        return {
            'title': conversation.title,
            'messages': conversation.messages
        }


@app.post('/conversation/{convo_id}/form')
async def send_form(request: Request, convo_id: int, prompt: Annotated[str, Form()]):
    with Session(engine) as session:
        # get the entire message history
        statement = select(Conversation).where(Conversation.id == convo_id)
        conversation: Conversation = session.exec(statement).first()
        # add the new message to the conversation
        message = Message(
            role='user',
            content=prompt,
            conversation_id=convo_id
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        # send the message to OpenAI
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=conversation.to_chatgpt()
        )
        response_message = response.choices[0].message
        new_message = Message(
            role=response_message['role'],
            content=response_message['content'],
            conversation_id=convo_id
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        # return the last message sent and the new message
        # as HTML
        return templates.TemplateResponse("form_response.html", {"request": request, "messages": [message.to_html(), new_message.to_html()]})


@app.post('/message')
async def create_message(message: Message):
    with Session(engine) as session:
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


@app.get('/message/{convo_id}')
async def get_message(convo_id: int):
    with Session(engine) as session:
        message = session.get(Message, convo_id)
        return message


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
