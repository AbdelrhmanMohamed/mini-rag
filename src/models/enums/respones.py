from enum import Enum


class ResponeseEnums(Enum):
    FILE_UPLOAD_SUCCESS = "success:uploaded done"
    FILE_UPLOAD_ERROR = "error:file type not supported"
    FILE_UPLOAD_LARGEST_SIZE = "error:file is largest size"
    FILE_UPLOAD_TYPE_NOT_SUPPORTED = "error:file type not supported"
