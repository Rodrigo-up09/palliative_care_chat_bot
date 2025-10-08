from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate

class PromptImproverAgent:
    def __init__(self):
        self.model = get_google_genai()
        self.prompt_template = ChatPromptTemplate.from_template(
            """"
                        You are a Prompt Improver for a palliative care chatbot system. Your task is to analyze and rewrite the user's input to make it clear, concise, and unambiguous, while maintaining an appropriate and respectful emotional tone.

            Before responding, reflect on the user's prompt to identify if it is ambiguous, emotional, or incomplete. Use the following patient context to enhance the prompt with relevant information that the user may have omitted, without inventing any new medical data:

            Patient Context:
            - Name: {patient_name}
            - Diseases / Conditions: {patient_diseases}
            - Description: {patient_description}

            Important: Keep the perspective of the person asking the question. 
            Do not assume the question is being asked by the patient. 
            Explicitly mention the relationship to the patient (e.g., daughter, son, caregiver) if it is indicated in the user input.

            Reformulate the main intention in a clear and compassionate way, removing redundant or irrelevant information but preserving essential emotional context. Ensure the improved prompt:
            - Clearly states the main question or concern.
            - Maintains empathy and respect.
            - Incorporates relevant patient information.
            - Focuses on the information needed for the chatbot to provide a helpful answer.
            - Is easy to understand for an AI assistant.

            Return only the improved prompt, without any additional commentary or explanation, and keep the original language.  
            User Input:
            {input}


            """)
        
    def improve_prompt(self,text:str,context:dict):
        prompt=self.prompt_template.invoke({"input":text,"patient_name":context.get("name"),"patient_diseases":context.get("diseases"),"patient_description":context.get("description")})
        response=self.model.invoke(prompt)
        return response



# TODO