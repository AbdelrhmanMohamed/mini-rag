from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """
    Abstract base class for LLM (Large Language Model) interfaces.
    This class defines the methods that any LLM interface should implement.
    """
    @abstractmethod
    def set_generation_model(self, model_id: str) -> None:
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int) -> None:
        pass

    @abstractmethod
    def generate_text(self, prompt: str, max_output_token: int, temprature: float) -> None:
        pass

    @abstractmethod
    def embed_text(self, txt: str, document_type: str) -> None:
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str) -> None:
        pass
