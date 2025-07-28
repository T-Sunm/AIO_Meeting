from enum import Enum


class LLMModel(Enum):
    """
    Enum for LLM models.
    """
    OPENAI_TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    OPENAI_GPT_4O_MLOPS5 = "gpt-4o-mlops5"
    OPENAI_GPT_4_1_MLOPS5 = "gpt-4.1-mlops5"
    OPENAI_GPT_3_5_MLOPS5 = "gpt-3.5-mlops5"
    

class LLMProvider(Enum):
    """
    Enum for LLM providers.
    """
    OPENAI = "openai"