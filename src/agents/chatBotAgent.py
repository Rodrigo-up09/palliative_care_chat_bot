from memory.messageState import ChatState
from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate
from utils.data_utils import DataUtils
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage

class ChatBotAgent:
    def __init__(self, csv):
        # Prompt template com placeholders para os 3 contextos + pergunta do usuário
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are a palliative care chatbot. Your role is to assist families who are caring for a patient at home under palliative care. "
                 "You will receive information in three separate contexts: "
                 "1) Theoretical knowledge: general guidelines and clinical knowledge about palliative care, "
                 "2) Patient-specific info: details about the individual patient, "
                 "3) Emotional context: information about the emotional state of the family or caregiver. "
                 "You should base your responses primarily on the provided theoretical context. "
                 "If you do not have information on a specific topic, state that the information is not available "
                 "and indicate that additional theoretical context should be added. "
                 "Always consider the emotional state of the family: if the situation is urgent or distressing, "
                 "summarize the information and be more direct rather than descriptive. Otherwise, you may provide "
                 "more detailed and descriptive answers. Prioritize the user's prompt above all.\n\n"
                 "Theoretical knowledge: {theoretical_context}\n"
                 "Patient-specific info: {individual_context}\n"
                 "Emotional context: {emotional_context}\n"
                 "User question: {user_query}")
            ]
        )

        self.data = DataUtils(csv)
        
        self.model = get_google_genai()
        
        # Criar workflow e memória persistente
        self.workflow = StateGraph(state_schema=ChatState)
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

        # Adicionar nó e aresta ao workflow
        self.workflow.add_node("model", self.call_model)
        self.workflow.add_edge(START, "model")

    def call_model(self, state: ChatState):
        """
        Função usada pelo workflow para gerar a resposta do modelo
        """
        # Combinar histórico de mensagens
        history_text = "\n".join([msg.content for msg in state["messages"]]) if state["messages"] else ""
        
        # Criar prompt final
        prompt = self.prompt_template.format(
            theoretical_context=state["theoretical_context"],
            individual_context=state["individual_context"],
            emotional_context=state["emotional_context"],
            user_query=history_text + "\n" if history_text else ""  # opcional incluir histórico
        )
        
        response = self.model(prompt)
        
        # s (necessário para LangGraph)
        return {"messages": [response]}

def generate_response(self, user_query: str, theoretical_context: str, user_id: int, emotional_context: str):
    # Obter contexto do paciente
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

    state = self.memory.load_state(thread_id=str(user_id))
    if state is None:
        # Estado inicial se ainda não existe
        state = ChatState(
            messages=[],
            theoretical_context=theoretical_context,
            individual_context=individual_context_text,
            emotional_context=emotional_context
        )
    else:
        # Atualizar contextos caso tenham mudado
        state["theoretical_context"] = theoretical_context
        state["individual_context"] = individual_context_text
        state["emotional_context"] = emotional_context

    # Adicionar a nova pergunta do usuário
    state["messages"].append(BaseMessage(content=user_query))

    # Invocar workflow
    output = self.app.invoke(state)

    # Salvar estado atualizado no MemorySaver
    self.memory.save_state(thread_id=str(user_id), state=state)

    # Retornar a última mensagem
    return output["messages"][-1].content
