from pydantic import BaseModel, Field
from typing import List

class MemoryRequest(BaseModel):
    title: str = Field(..., description="The title of the memory.")
    content: str = Field(..., description="The content of the memory.")

class ImportRequest(BaseModel):
    memories: List[MemoryRequest] = Field(..., description="A list of memories to import.")
