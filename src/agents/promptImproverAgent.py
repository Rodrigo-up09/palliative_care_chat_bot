from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate

class PromptImproverAgent:
    def __init__(self):
        self.model = get_google_genai()
        self.prompt_template = ChatPromptTemplate.from_template(
            """"
            You are a Prompt Improver for a palliative care chatbot system. Your task is to analyze and rewrite the user's input to make it as clear, concise, and unambiguous as possible, while maintaining an appropriate and respectful emotional tone. 

            Before responding, reflect on the user's prompt to identify if it is ambiguous, emotional, or incomplete. Then, reformulate the main intention in a clear and compassionate way, removing redundant or irrelevant information but preserving essential emotional context.
            Ensure the improved prompt:
            - Clearly states the main question or concern.
            - Maintains empathy and respect.
            - Focuses on the information needed for the chatbot to provide a helpful answer.
            - Is easy to understand for an AI assistant.


            Return only the improved prompt, without any additional commentary or explanation  and keep the original language.
            Passage:
            {input}

            """)
        
    def improve_prompt(self,text:str):
        prompt=self.prompt_template.invoke({"input":text})
        response=self.model.invoke(prompt)
        return response



# TODO