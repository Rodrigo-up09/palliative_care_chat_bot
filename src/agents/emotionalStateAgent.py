from langchain.prompts.chat import ChatPromptTemplate
from models.llm_factory import get_google_genai
from pydantic import BaseModel, Field

class Classification(BaseModel):
    emotion: int = Field(
        description=(
            "Represents the family's emotional intensity or level of distress on a scale from 1 to 10. "
            "A low value (1–3) indicates a calm or curious state — the family is simply seeking information. "
            "A medium value (4–7) reflects concern or anxiety — the family needs reassurance and clear guidance. "
            "A high value (8–10) represents a state of urgency or desperation — the family is emotionally overwhelmed "
            "and needs concise, direct, and comforting recommendations rather than long explanations."
        )
    )

class EmotionalStateAgent:
    def __init__(self):
        self.prompt_template = ChatPromptTemplate.from_template(
                """
            Extract the desired information from the following passage.

            Only extract the properties mentioned in the 'Classification' function.

            Passage:
            {input}
            """)
        model=get_google_genai()
        self.model = model.with_structured_output(Classification)

    def classify_emotion(self, text: str) -> int:
        prompt = self.prompt_template.invoke({"input": text})
        response = self.model.invoke(prompt)
        return response


        

