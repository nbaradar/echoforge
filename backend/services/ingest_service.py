from models.import_models import ImportRequest
from db.imports import ImportService
from fastapi import Depends
from bson import ObjectId

class IngestionService:
    def __init__(self, import_service: ImportService = Depends(ImportService)):
        self.import_service = import_service

    async def process_import(self, import_request: ImportRequest):
        # In a real application, the user_id would come from an auth system.
        # For the POC, we'll use a hardcoded ObjectId.
        # You can create one using: `import bson; print(bson.ObjectId())`
        # This will eventually be a foreign key that corresponds to the user object primary key. bson just converts it to a readable mongo ObjectId.
        user_id = ObjectId("66886a755c62381a7e728e8a") # Replace with a valid ObjectId

        import_doc = await self.import_service.create_import(user_id, import_request)

        return {
            "status": "success",
            "message": "Import job created successfully.",
            "import_id": str(import_doc.id)
        }