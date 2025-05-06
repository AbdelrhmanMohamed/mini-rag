from .BaseDataModel import BaseDataModel
from .db_schemes import ProjectSchema
from motor.motor_asyncio import AsyncIOMotorCollection


class ProjectModel(BaseDataModel):
    def __init__(self, db_client=AsyncIOMotorCollection):
        super().__init__(db_client=db_client)
        self.collection_name = "projects"
        self.collection = self.db_client[self.collection_name]

    # Create indexes for the collection
    # TODO: NOT COMPLETED
    async def create_indexes(self):
        indexes = ProjectSchema.get_indexses()
        existing_indexes = await self.collection.index_information()
        existing_index_names = set(existing_indexes.keys())
        for index in indexes:
            index_name = index["name"]
            if index_name in existing_index_names:
                print(f"Index {index_name} already exists, skipping creation.")
                continue
            await self.collection.create_index(
                index["key"],
                name=index["name"],
                unique=index["unique"],
                sparse=index["sparse"]
            )

    async def create_project(self, project: ProjectSchema):
        result = await self.collection.insert_one({
            "project_id": project.project_id
        })
        project.id = result.inserted_id

        return project

    async def get_project_one_create(self, project_id: str):
        record = await self.collection.find_one({
            "project_id": project_id
        })
        project = ProjectSchema(project_id=project_id)
        print(record, 'record')
        project.id = record["_id"]
        if record is None:
            project = ProjectSchema(project_id=project_id)
            result = await self.create_project(project)
            project.id = result.id
            return project

        return project
