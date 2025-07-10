from pydantic import BaseModel


class AIPrompt(BaseModel):
    prompt: str


class MemoryCreate(BaseModel):
    topic: str
    content: str
    summary: str | None = None
