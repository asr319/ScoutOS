from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session
from .auth import get_current_user
from .websocket_manager import manager
from .consent import get_consent_message
from .database import SessionLocal
from .ai import save_prompt, save_memory, get_memories_by_topic
from .schemas import AIPrompt, MemoryCreate
import logging


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/handshake")
async def handshake(user_id: str = Depends(get_current_user)):
    logging.info(f"Handshake request for user {user_id}")
    return {"message": f"Handshake successful for user {user_id}"}


@router.get("/dashboard")
async def dashboard():
    from .metrics_utils import get_storage_usage, get_active_users_count

    active_users = await get_active_users_count()
    used_bytes, total_bytes = await get_storage_usage("/")
    return {
        "active_users": active_users,
        "storage_used_bytes": used_bytes,
        "storage_total_bytes": total_bytes,
    }


@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
):
    content = await file.read()
    lines = content.decode('utf-8', errors='ignore').splitlines()
    repaired_lines = [line for line in lines if line.strip()]
    logging.info(
        "User %s uploaded document with %d lines processed.",
        user_id,
        len(repaired_lines),
    )
    return {
        "message": "Document processed",
        "lines_processed": len(repaired_lines),
    }


@router.get("/consent-message")
async def consent_message(lang: str = Query("en")):
    return {"message": get_consent_message(lang)}


@router.post("/ai/prompt")
async def ai_prompt(
    data: AIPrompt,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    response = data.prompt[::-1]
    save_prompt(db, user_id, data.prompt, response)
    return {"response": response}


@router.post("/memory")
async def create_memory(
    memory: MemoryCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    save_memory(db, user_id, memory.topic, memory.content, memory.summary)
    return {"message": "Memory saved"}


@router.get("/memory/{topic}")
async def read_memory(
    topic: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mems = get_memories_by_topic(db, user_id, topic)
    return {
        "memories": [
            {
                "id": m.id,
                "topic": m.topic,
                "summary": m.summary,
                "content": m.content,
                "created_at": m.created_at,
            }
            for m in mems
        ]
    }


@router.post("/request-merge")
async def request_merge(
    user_id: str = Depends(get_current_user),
    merge_info: dict = None,
):
    logging.info(f"Merge request from user {user_id}: {merge_info}")
    await manager.send_personal_message(
        "Merge request requires your approval.",
        user_id,
    )
    return {"message": "Merge request sent for user approval."}


@router.post("/approve-merge")
async def approve_merge(
    user_id: str = Depends(get_current_user),
    approved: bool = False,
):
    if not approved:
        logging.info(f"User {user_id} denied merge.")
        return {"message": "Merge denied by user."}
    logging.info(f"User {user_id} approved merge.")
    return {"message": "Merge completed."}


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
