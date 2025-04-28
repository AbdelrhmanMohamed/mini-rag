from .BaseController import BaseController
from fastapi import UploadFile
from models.enums.respones import ResponeseEnums


class DataController(BaseController):
    def __init__(self):
        self.scale_size = 1048576
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponeseEnums.FILE_UPLOAD_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.scale_size:
            return False, ResponeseEnums.FILE_UPLOAD_SIZE_EXCEEDED.value
        return True, ResponeseEnums.FILE_UPLOAD_SUCCESS.value
