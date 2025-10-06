from memory.messageState import ChatState
from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate
from utils.data_utils import DataUtils
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from langgraph.graph import START, MessagesState, StateGraph
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

class ChatBotAgent:
    def __init__(self, csv):
        # Prompt template com placeholders para os 3 contextos + pergunta do usuário
        self.prompt_template = ChatPromptTemplate.from_messages([
        ("system",
        "You are a palliative care chatbot assisting families caring for a patient at home. "
        "You receive three contexts:\n"
        "1) Theoretical knowledge: general palliative care guidelines.\n"
        "2) Patient-specific info: details about the patient.\n"
        "3) Emotional context: family stress level (1-10).\n\n"
        "Instructions:\n"
        "- Base your answers primarily on the theoretical context.\n"
        "- Do NOT repeat patient-specific info unnecessarily.\n"
        "- Adjust your response based on emotional context:\n"
        "    * 8-10: family is in distress/desperate – give **direct, concise recommendations**, avoid long explanations.\n"
        "    * 4-7: family is somewhat anxious – give **clear guidance with moderate explanation**.\n"
        "    * 1-3: family is calm – you may give **more detailed and descriptive answers**.\n"
        "- Prioritize user questions, provide actionable steps first, then optional elaboration if emotional context allows.\n\n"
        "Theoretical knowledge: {theoretical_context}\n"
        "Patient-specific info: {individual_context}\n"
        "Emotional context: {emotional_context}\n"),
        MessagesPlaceholder(variable_name="messages"),
        ])
        

        self.data = DataUtils(csv)
        
        self.model = get_google_genai()
        
        # Criar workflow e memória
        self.workflow = StateGraph(state_schema=ChatState)
       

        # Adicionar nó e aresta ao workflow
    
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

    def call_model(self, state: ChatState):
        # Passar a lista de mensagens diretamente
        prompt = self.prompt_template.format(
            theoretical_context=state["theoretical_context"],
            individual_context=state["individual_context"],
            emotional_context=state["emotional_context"],
            messages=state["messages"]
        )

        # invoke retorna um objeto de geração, precisamos do texto
        model_output = self.model.invoke(prompt)
        
        return {"messages": [model_output]}





    def generate_response(self, user_query: str, theoretical_context: str, user_id: int, emotional_context: str):
        individual_context = self.data.get_full_patient_info(user_id)
        if individual_context is None:
            individual_context_text = "No patient-specific information available."
        else:
            individual_context_text = (
                f"Name: {individual_context['patient_name']}, "
                f"Diseases: {individual_context['patient_diseases']}, "
                f"Description: {individual_context['patient_description']}"
            )

        # Recuperar histórico do MemorySaver para este user_id

        state = ChatState(
        messages=[HumanMessage(content=user_query)],
        theoretical_context=theoretical_context,
        individual_context=individual_context_text,
        emotional_context=emotional_context
    )
        config = {"configurable": {"thread_id": str(user_id)}}

        output = self.app.invoke(state, config)
        

      

        return output["messages"][-1].pretty_print()






