from .BaseController import BaseController
from .ProjectController import ProjectContoller
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectContoller().get_project_path(project_id=project_id)

    def get_file_ext(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_ext(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)
        print(f"file_path: {file_path}")
        if file_ext == ".txt":
            return TextLoader(file_path)

        if file_ext == ".pdf":
            return PyPDFLoader(file_path)

        return None

    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id)
        return loader.load()

    def process_file(self, file_content: list,  chunk_size: int = 100, overlap_size: int = 50):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
            is_separator_regex=False,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]
        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts, metadatas=file_content_metadata)

        serializable_chunks = [
            {"page_content": chunk.page_content, "metadata": chunk.metadata}
            for chunk in chunks
        ]

        return chunks
