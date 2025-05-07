from enum import Enum


class LLMModelType(Enum):
    """Enum for LLM model types."""
    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"
