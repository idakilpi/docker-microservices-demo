from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Note(BaseModel):
    title: str
    body: str

notes = []

@app.get("/notes", response_model=List[Note])
def get_notes():
    return notes

@app.post("/notes", response_model=Note)
def add_note(note: Note):
    notes.append(note)
    return note