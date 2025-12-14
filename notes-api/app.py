import json
import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lisätään ID-kenttä malliin
class Note(BaseModel):
    id: Optional[str] = None
    title: str
    body: str

DATA_FILE = "/data/notes.json"

def load_notes_from_file():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_notes_list(notes_list):
    with open(DATA_FILE, "w") as f:
        json.dump(notes_list, f, indent=4)

@app.get("/notes", response_model=List[Note])
def get_notes():
    return load_notes_from_file()

@app.post("/notes", response_model=Note)
def add_note(note: Note):
    # Luodaan uniikki ID (UUID)
    note.id = str(uuid.uuid4())
    
    current_notes = load_notes_from_file()
    # Tallennetaan sanakirjana (dict)
    current_notes.append(note.dict())
    save_notes_list(current_notes)
    
    return note

# Poistotoiminto
@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    current_notes = load_notes_from_file()
    
    # Suodatetaan lista: pidetään vain ne, joiden ID EI ole se poistettava
    updated_notes = [n for n in current_notes if n.get("id") != note_id]
    
    if len(current_notes) == len(updated_notes):
        raise HTTPException(status_code=404, detail="Note not found")

    save_notes_list(updated_notes)
    return {"message": "Note deleted"}