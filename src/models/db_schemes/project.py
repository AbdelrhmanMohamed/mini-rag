from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import PyObjectId
from bson import ObjectId


class ProjectSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    project_id: str = Field(min_length=1)

    @field_validator('project_id', mode='after')
    @classmethod
    def check_project_id_match(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }
