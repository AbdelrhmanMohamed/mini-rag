from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunkSchema
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import InsertOne
from bson.objectid import ObjectId
from typing import List


class ChunkModel(BaseDataModel):
    def __init__(self, db_client=AsyncIOMotorCollection):
        super().__init__(db_client=db_client)
        self.collection_name = "chunks"
        self.collection = self.db_client[self.collection_name]

    async def create_chunk(self, chunk: DataChunkSchema):
        result = await self.collection.insert_one(chunk.model_dump())
        chunk.id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        record = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if record is None:
            return None

        return DataChunkSchema(**record)

    async def create_many_chunk(self, chunks: List[DataChunkSchema], batch_size: int = 100) -> int:

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            operations = [InsertOne(chunk.model_dump()) for chunk in batch]

            await self.collection.bulk_write(operations)

        return len(chunks)

    async def delete_many_chunks(self, project_id: str):
        print(type(project_id), 'project_id')
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        return result

    async def get_all_chunks(self, project_id: str):
        cursor = self.collection.find({
            "chunk_project_id": project_id
        })

        chunks = []
        async for doc in cursor:
            print(doc, 'content4444')
            chunks.append(doc)

        return []
