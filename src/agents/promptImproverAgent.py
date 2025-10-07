from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate

class PromptImproverAgent:
    def __init__(self):
        self.model = get_google_genai()
        self.prompt_template = ChatPromptTemplate.from_template(
            """"
            You are a Prompt Improver for a palliative care chatbot system. Your task is to rewrite the user's input to make it as clear, concise, and unambiguous as possible, removing redundant or irrelevant information. Ensure the improved prompt:
            - Clearly states the main question or concern.
            - Avoids emotional or repetitive language unless it is essential for context.
            - Focuses on the specific information needed for the chatbot to provide a helpful answer.
            - Is easy to understand for an AI assistant.
            Return only the improved prompt, without any additional commentary or explanation.

            """)

# TODO