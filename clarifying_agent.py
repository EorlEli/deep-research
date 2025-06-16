from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a helpful assistant. Given a research query, generate 2-4 clarifying questions that would help make the research more relevant and focused. "
    "Ask for any missing context, specifics, or goals that would help clarify the user's intent. "
    "Return only the questions, not the answers."
)

class ClarifyingQuestions(BaseModel):
    questions: list[str] = Field(description="A list of clarifying questions to ask the user.")

clarifying_agent = Agent(
    name="ClarifyingAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
) 