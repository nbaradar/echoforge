from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Import(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    raw_content: List[Dict[str, Any]]
    source_provider: str
    import_type: str
    import_trigger: str
    import_session: str
    source_prompt_id: Optional[PyObjectId] = None
    num_memories: int
    status: str = "pending"
    processing_notes: Optional[str] = None
    is_duplicate: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Prompt(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    content: str
    description: Optional[str] = None
    tags: List[str] = []
    scope: str
    owner_id: Optional[PyObjectId] = None
    persona_id: Optional[PyObjectId] = None
    version: int = 1
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Log(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    event_type: str
    user_id: PyObjectId
    import_id: Optional[PyObjectId] = None
    memory_id: Optional[PyObjectId] = None
    prompt_id: Optional[PyObjectId] = None
    details: Dict[str, Any]
    level: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
