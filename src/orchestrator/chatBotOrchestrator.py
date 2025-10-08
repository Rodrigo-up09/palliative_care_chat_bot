from agents.chatBotAgent import ChatBotAgent
from agents.emotionalStateAgent import EmotionalStateAgent
from agents.infoFetcher import InfoFetcherAgent
from agents.promptImproverAgent import PromptImproverAgent
from agents.summarizeAgent import SummarizeAgent
from utils.data_utils import DataUtils


class ChatbotOrchestrator:
    def __init__(self,csv):
        self.prompt_improver = PromptImproverAgent()
        self.info_fetcher = InfoFetcherAgent()
        self.summarizer = SummarizeAgent()  
        self.chatBot= ChatBotAgent()
        self.emotional_bot=EmotionalStateAgent()
        self.data=DataUtils(csv)


    async def handle_user_input(self, user_raw_input: str, user_id: str,theoretical_context):

        context=self.data.get_full_patient_info(user_id)

        print(f"Patient Context: {context}\n")

        improve_input = self.prompt_improver.improve_prompt(user_raw_input,context={
                "name": context.get("patient_name"),
                "diseases": context.get("patient_diseases"),
                "description": context.get("patient_description")}
    )

        print(f"Improved Prompt: {improve_input.content}\n")

        emotion=self.emotional_bot.classify_emotion(user_raw_input)

        print(f"Emotion: {emotion}\n")
        self.info_fetcher.add_documents(theoretical_context)
        docs = self.info_fetcher.retrieve(improve_input.content, top_k=5)

        print(f"Retrieved Documents: {[doc.page_content[:100] for doc in docs]}\n")

        response = self.chatBot.generate_response(
            user_query=improve_input.content,
            theoretical_context=docs,
            user_id=user_id,
            emotional_context=str(emotion)
        )

        return response




    async def chat_loop(self, user_id: str, theoretical_context: str):
        """
        Loop para simular o chatbot completo.

        Args:
            chat_system: instância que possui o método handle_user_input.
            user_id: ID do paciente/usuário.
            theoretical_context: texto ou tema para busca no InfoFetcher.
        """
        print("Chatbot iniciado! Digite 'sair' para encerrar.\n")
        while True:
            user_input = input("Você: ")
            if user_input.lower() in ("sair", "exit", "quit"):
                print("Encerrando o chatbot. Até logo!")
                break

            # Chama a função assíncrona para processar input
            response_content = await self.handle_user_input(
                user_raw_input=user_input,
                user_id=user_id,
                theoretical_context=theoretical_context
            )

            print(f"Chatbot: {response_content}\n")
