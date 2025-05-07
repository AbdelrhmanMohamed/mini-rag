from openai import OpenAI
from ..LLMInterface import LLMInterface
from logging import getLogger


class OpenAIProvider(LLMInterface):
    """
    OpenAIProvider is a concrete implementation of the LLMInterface for OpenAI's API.
    It provides methods to set generation and embedding models, generate text, embed text,
    and construct prompts using OpenAI's services.
    """

    def __init__(self, api_key: str, api_url: str = None, default_input_max_chracter: int = 1000,
                 default_output_max_tokens: int = 1000, default_generation_temprature: float = 0.1) -> None:
        # Parameters:
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_chracter = default_input_max_chracter
        self.default_output_max_tokens = default_output_max_tokens
        self.default_generation_temprature = default_generation_temprature
        # model generation and embedding
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.openai = OpenAI(api_key=self.api_key, api_url=self.api_url)

        # Initialize logger
        self.logger = getLogger(__name__)
        self.logger.info("OpenAIProvider initialized with API key and URL.")

    def set_generation_model(self, model_id: str) -> None:
        self.generation_model_id = model_id
        self.logger.info(f"Generation model set to: {model_id}")

    def set_embedding_model(self, model_id: str, embedding_size: int) -> None:
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        self.logger.info(f"Embedding model set to: {model_id}")

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None) -> str:
        if not self.openai:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.default_generation_temprature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role="user")
        )

        response = self.openai.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message["content"]

    def embed_text(self, txt: str, document_type: str) -> list:
        if self.openai is None:
            raise ValueError(
                "Embedding model ID is not set. Please set it before embedding text.")
        if self.embedding_model_id is None:
            raise ValueError(
                "Embedding model ID is not set. Please set it before embedding text.")
        response = self.openai.embeddings.create(
            model=self.embedding_model_id,
            input=txt,
            user=document_type
        )
        if response is None or response.data[0].embedding is None or len(response.data[0].embedding) == 0:
            self.logger.error("Failed to embed text.")
            return None

        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

    def process_text(self, text: str):
        return text[:self.default_input_max_chracter].strip()
