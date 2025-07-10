from fastapi import APIRouter, UploadFile, File, Depends, Query, WebSocket, WebSocketDisconnect, HTTPException
from .auth import get_current_user
from .websocket_manager import manager
from .consent import get_consent_message
import logging

router = APIRouter()

@router.get("/handshake")
async def handshake(user_id: str = Depends(get_current_user)):
    logging.info(f"Handshake request for user {user_id}")
    return {"message": f"Handshake successful for user {user_id}"}

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    content = await file.read()
    lines = content.decode('utf-8', errors='ignore').splitlines()
    repaired_lines = [line for line in lines if line.strip()]
    logging.info(f"User {user_id} uploaded document with {len(repaired_lines)} lines processed.")
    return {"message": "Document processed", "lines_processed": len(repaired_lines)}

@router.get("/consent-message")
async def consent_message(lang: str = Query("en")):
    return {"message": get_consent_message(lang)}

@router.post("/request-merge")
async def request_merge(user_id: str = Depends(get_current_user), merge_info: dict = {}):
    logging.info(f"Merge request from user {user_id}: {merge_info}")
    await manager.send_personal_message("Merge request requires your approval.", user_id)
    return {"message": "Merge request sent for user approval."}

@router.post("/approve-merge")
async def approve_merge(user_id: str = Depends(get_current_user), approved: bool = False):
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
