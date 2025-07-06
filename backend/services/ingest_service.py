import logging
from schemas.requests import ImportRequest
from schemas.responses import ImportResponse
from db.imports import ImportService
from fastapi import Depends, HTTPException
from bson import ObjectId
from utils.import_parser import parse_raw_import_data
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self, import_service: ImportService = Depends(ImportService)):
        self.import_service = import_service

    async def process_import(self, raw_data: Dict[str, Any]) -> ImportResponse:
        import_request: ImportRequest
        failed_memories: List[Dict[str, Any]] = []
        try:
            import_request, failed_memories = parse_raw_import_data(raw_data)
            logger.info(f"Successfully parsed {len(import_request.memories)} memories from raw data. {len(failed_memories)} memories failed to parse.")
        except ValueError as e:
            logger.error(f"Failed to parse raw import data: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"An unexpected error occurred during raw data parsing: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during data parsing.")

        # In a real application, the user_id would come from an auth system.
        # For the POC, we'll use a hardcoded ObjectId.
        user_id = ObjectId("6869ab95ba829ecd62853fe2") 

        try:
            import_doc = await self.import_service.create_import(user_id, import_request)
            message = f"Import job created successfully. {len(import_request.memories)} memories processed."
            if failed_memories:
                message += f" However, {len(failed_memories)} memories failed to parse and were skipped."
                logger.warning(f"Import completed with skipped memories. Failed memories: {failed_memories}")
            logger.info(f"Import process completed for import_id: {import_doc.id}. Status: success.")
            return ImportResponse(
                status="success",
                message=message,
                import_id=str(import_doc.id)
            )
        except Exception as e:
            logger.error(f"Failed to create import record in DB for user_id: {user_id}. Error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to create import record: {e}")