from sqlalchemy.orm import Session
from typing import List

from .models import Prompt, Memory
from .database import Base, engine

Base.metadata.create_all(bind=engine)


def save_prompt(db: Session, user_id: str, prompt: str, response: str) -> Prompt:
    db_prompt = Prompt(
        user_id=user_id, prompt_text=prompt, response_text=response
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def save_memory(
    db: Session,
    user_id: str,
    topic: str,
    content: str,
    summary: str | None = None,
) -> Memory:
    """Persist a memory entry for later retrieval."""

    db_memory = Memory(
        user_id=user_id,
        topic=topic,
        content=content,
        summary=summary,
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


def get_memories_by_topic(
    db: Session, user_id: str, topic: str
) -> List[Memory]:
    """Return memories for a user filtered by topic."""

    return (
        db.query(Memory)
        .filter(Memory.user_id == user_id, Memory.topic == topic)
        .order_by(Memory.created_at.desc())
        .all()
    )
