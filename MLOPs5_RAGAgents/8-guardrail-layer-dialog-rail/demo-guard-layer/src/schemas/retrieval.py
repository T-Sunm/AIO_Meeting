from pydantic import BaseModel, Field
from typing import Optional


class RetrievalInput(BaseModel):
    user_input: str = Field(
        description="User input",
        default="What do beetles eat?",
    )
    session_id: Optional[str] = Field(
        description="Session ID for tracking user sessions",
        default=None,
    )
    user_id: Optional[str] = Field(
        description="User ID for tracking user sessions",
        default=None,
    )
