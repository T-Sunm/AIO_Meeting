from langchain.chat_models import init_chat_model
from src.settings import SETTINGS
from langchain_openai import ChatOpenAI
# Initialize the LLM with the specified model and settings
# This code initializes a chat model using the OpenAI API with specific parameters.
# The model used is "gpt-4o-mini", with a temperature setting of 0.7 for response variability.
llm = ChatOpenAI(
    openai_api_base="http://127.0.0.1:1234/v1",
    openai_api_key="lm-studio",
    model_name="Tên_model_trên_LMStudio",
    temperature=0.7,
)
