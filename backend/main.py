from fastapi import FastAPI
from pydantic import BaseModel
from agent import process_user_input

app = FastAPI()

class UserMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(user_message: UserMessage):
    reply = await process_user_input(user_message.message)
    return {"response": reply}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Calendar Booking Chatbot API"}
