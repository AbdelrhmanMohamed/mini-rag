from pydantic import BaseModel, Field
from typing import Optional
from .base import PyObjectId
from bson import ObjectId


class DataChunkSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    chunk_text: str = Field(min_length=1)
    chunk_metadata: dict
    order: int = Field(gt=0)
    chunk_project_id:  str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }

    @classmethod
    def get_indexses(cls):
        return [
            {
                "key": [("chunk_project_id", 1)],
                "name": "chunk_project_id_index_1",
                "unique": False,
                # "sparse": True
            }
        ]
