from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from .database import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Memory(Base):
    """Long-lived memory entries for the AI agent."""

    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    topic = Column(String, index=True)
    summary = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
