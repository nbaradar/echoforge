from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.db_models import Import
from schemas.requests import ImportRequest
from db.client import db_client
from bson import ObjectId
import uuid

class ImportService:
    def __init__(self, db: AsyncIOMotorDatabase = Depends(db_client.get_db)):
        self.db = db

    async def create_import(self, user_id: ObjectId, import_request: ImportRequest) -> Import:
        """
        Creates a new import record in the database.
        """
        import_session = f"sess_{uuid.uuid4()}"
        
        import_doc = Import(
            user_id=user_id,
            raw_content=[memory.dict() for memory in import_request.memories],
            source_provider="openai", # Hardcoded for now
            import_type="provider", # Hardcoded for now
            import_trigger="manual", # Hardcoded for now
            import_session=import_session,
            num_memories=len(import_request.memories),
        )

        await self.db.imports.insert_one(import_doc.dict(by_alias=True))
        return import_doc
