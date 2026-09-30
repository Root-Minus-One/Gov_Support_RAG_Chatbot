from pydantic import BaseModel, Field

# Shared / Sub-Models
class Citation(BaseModel):
    chunk_id: str
    doc_id: str
    document_title: str
    page_number: int | None = None
    category: str


# Request Models (Inputs)
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The user's input question.")
    session_id: str = Field(..., description="Unique session ID for chat history.")
    user_id: str = Field(..., description="User ID for trace tracking.")
    category: str | None = Field(default=None, description="Optional program category filter.")

# class ChatRequest(BaseModel):
#     question : str
#     category : Optional[str] = None
#     session_id : Optional[str] = Field(
#         default=None,
#         description="Optional session UUID. Leave null to generate a new session."
#     )


# Response Models (Outputs)
class ChatResponse(BaseModel):
    success: bool = Field(
        ..., description="True if request completed cleanly, False for input/internal errors."
    )
    is_relevant: bool = Field(
        default=True,
        description="False if the question was rejected as out-of-scope.",
    )
    answer: str = Field(
        ..., description="The generated LLM answer or refusal message."
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Source document citations (empty if irrelevant or on error).",
    )
    trace_id: str | None = Field(
        default=None,
        description="Langfuse trace ID for user feedback matching.",
    )
    error_message: str | None = Field(
        default=None,
        description="Populated only when success is False.",
    )