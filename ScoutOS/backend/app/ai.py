from sqlalchemy.orm import Session

from .models import Prompt
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
