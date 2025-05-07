
from .LLMEnums import LLMModelType
from .providers import OpenAIProvider


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLMModelType.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_chracter=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temprature=self.config.GENERATION_DAFAULT_TEMPERATURE,
            )

        if provider == LLMModelType.COHERE.value:
            raise NotImplementedError(
                "Cohere provider is not implemented yet.")

        return None
