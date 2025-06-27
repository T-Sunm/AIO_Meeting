from pydantic import BaseModel, Field


class RetrievalInput(BaseModel):
    user_input: str = Field(
        description="User input",
        default="What do beetles eat?",
    )
