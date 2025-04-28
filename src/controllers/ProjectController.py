from .BaseController import BaseController
import os
import random
import string
import re


class ProjectContoller(BaseController):
    def __init__(self):
        super().__init__()

    def generate_safe_filename(base_name: str, extension: str = "pdf") -> str:
        # Generate random 8-character string
        random_str = ''.join(random.choices(
            string.ascii_letters + string.digits, k=8))

        # Replace unsafe characters with underscores
        safe_base = re.sub(r'[^A-Za-z0-9_\-]', '_', base_name)

        # Assemble filename
        filename = f"{safe_base}_{random_str}.{extension}"
        return filename

    def get_project_path(self, project_id: str):
        project_dir = os.path.join(self.files_dir, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
