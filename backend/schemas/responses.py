from pydantic import BaseModel

class ImportResponse(BaseModel):
    import_id: str
    status: str
    message: str
