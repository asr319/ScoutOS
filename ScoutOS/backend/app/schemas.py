from pydantic import BaseModel


class AIPrompt(BaseModel):
    prompt: str
