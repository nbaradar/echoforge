from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.requests import ImportRequest
from schemas.responses import ImportResponse
from services.ingest_service import IngestionService

router = APIRouter()

@router.post("/import")
async def import_memories(
    raw_data: dict,
    ingestion_service: IngestionService = Depends(IngestionService)
) -> ImportResponse:
    """
    Imports a list of memories and stores them in the database.
    """
    try:
        result = await ingestion_service.process_import(raw_data)
        return result
    except Exception as e:
        # In a real app, you'd want more specific error handling
        raise HTTPException(status_code=500, detail=str(e))