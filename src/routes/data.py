from fastapi import APIRouter, UploadFile, status, Depends, Request
from fastapi.responses import JSONResponse
from controllers.DataController import DataController
from controllers.ProjectController import ProjectContoller
from controllers.ProcessController import ProcessController
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunkSchema
import os
from helpers.config import get_settings, Settings
import aiofiles  # type: ignore
from models.enums.respones import ResponeseEnums
import logging
from .schemes.data import ProcessRequest
from models.db_schemes import ProjectSchema
import json
from typing import List
from bson import ObjectId

logger = logging.getLogger("uvuicon.error")
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str,  file: UploadFile, app_settings: Settings = Depends(get_settings)):
    if not file:
        return JSONResponse(
            status_code=status.HTTP_304_NOT_MODIFIED,
            content={
                "signal": "please upload file"
            })
    isValid, restlt_msg = DataController().validate_uploaded_file(file)
    if not isValid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": restlt_msg
            })
    project_model = ProjectModel(db_client=request.app.db_client)
    await project_model.create_project(ProjectSchema(**{
        "project_id": project_id
    }))
    project_dir_path = ProjectContoller().get_project_path(project_id)
    safe_file_name = ProjectContoller.generate_safe_filename(file.filename)
    file_path = os.path.join(project_dir_path, safe_file_name)
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHANUK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"erro while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponeseEnums.FILE_UPLOAD_ERROR.value
            })

    return JSONResponse(
        content={
            "signal": ResponeseEnums.FILE_UPLOAD_SUCCESS.value,
            "file_id": safe_file_name
        })


@data_router.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_request: ProcessRequest, app_settings: Settings = Depends(get_settings)):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    project_model = ProjectModel(db_client=request.app.db_client)
    chunk_model = ChunkModel(db_client=request.app.db_client)
    project = await project_model.get_project_one_create(project_id=project_id)
    print(str(project.id), 'project idddddddd')
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file(
        file_content=file_content, chunk_size=chunk_size, overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            content={
                "signal": ResponeseEnums.FILE_PROCESS_ERROR.value,
                "file_id": file_id,
                'message': 'file content is empty'})
    try:
        if do_reset == 1:
            print("do reset")
            _ = await chunk_model.delete_many_chunks(project_id=str(project.id))
    except Exception as e:
        print(f"Failed to delete chunks: {e}")
        return
    file_chunks_records: List[DataChunkSchema] = []
    for index, chunk in enumerate(file_chunks):
        record = DataChunkSchema(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            order=index + 1,
            chunk_project_id=str(project.id))
        file_chunks_records.append(record)

    rum_records = await chunk_model.create_many_chunk(file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponeseEnums.FILE_PROCESS_SUCCESS.value,
            "rum_records": rum_records}
    )


@data_router.get("/project/get/{project_id}")
async def get_project(request: Request, project_id: str, app_settings: Settings = Depends(get_settings)):
    project_model = ProjectModel(db_client=request.app.db_client)
    chunk_model = ChunkModel(db_client=request.app.db_client)
    project = await chunk_model.get_all_chunks(project_id=project_id)
    print(project, 'project')
    return "00"
