from schemas.requests import ImportRequest
from schemas.responses import ImportResponse
from db.imports import ImportService
from fastapi import Depends
from bson import ObjectId

class IngestionService:
    def __init__(self, import_service: ImportService = Depends(ImportService)):
        self.import_service = import_service

    async def process_import(self, import_request: ImportRequest):
        # In a real application, the user_id would come from an auth system.
        # For the POC, we'll use a hardcoded ObjectId.

        # This is a foreign key that corresponds to the user object primary key.
        user_id = ObjectId("6869ab95ba829ecd62853fe2") 

        import_doc = await self.import_service.create_import(user_id, import_request)

        return ImportResponse(
            status="success",
            message="Import job created successfully.",
            import_id=str(import_doc.id)
        )