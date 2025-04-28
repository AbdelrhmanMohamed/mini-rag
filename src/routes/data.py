from fastapi import APIRouter, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from controllers.DataController import DataController
from controllers.ProjectController import ProjectContoller
import os
from helpers.config import get_settings, Settings
import aiofiles  # type: ignore
from models.enums.respones import ResponeseEnums
import logging

logger = logging.getLogger("uvuicon.error")


data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,  file: UploadFile, app_settings: Settings = Depends(get_settings)):
    isValid, restlt_msg = DataController().validate_uploaded_file(file)
    if not isValid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": restlt_msg
            })

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
