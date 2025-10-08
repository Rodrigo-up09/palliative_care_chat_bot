from agents.chatBotAgent import ChatBotAgent
from agents.emotionalStateAgent import EmotionalStateAgent
from agents.infoFetcher import InfoFetcherAgent
from agents.promptImproverAgent import PromptImproverAgent
from agents.summarizeAgent import SummarizeAgent
from utils.docs_utils import split_documentForEmbedding
from utils.data_utils import DataUtils
from orchestrator.chatBotOrchestrator import ChatbotOrchestrator
def testChatBot():
    agent = ChatBotAgent("data/clinic_cases.csv")  # Caminho para o CSV
    user_id = 1
    theoretical_context = "General guidelines on palliative care."
    emotional_context = "10"

    print("ChatBot iniciado! Escreva 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "quit", "exit"]:
            break

        response = agent.generate_response(
            user_query=user_input,
            theoretical_context=theoretical_context,
            user_id=user_id,
            emotional_context=emotional_context
        )

        print("ChatBot:", response)




def testEmotionBot():
    agent = EmotionalStateAgent()
    test_cases = [
        "Já não sei se o que estão a fazer é ajudar ou só prolongar o sofrimento… não quero ser injusto, mas dói tanto ver isto.",
        "Ela estava melhor ontem e agora dizem que é o fim? Como é que se entende isto? Não faz sentido nenhum.",
        "Disseram-me que iam mudar o tratamento, mas ninguém me disse porquê… é bom ou mau?",
        "Ela já não come, mas dizem que é normal. Normal como? Para quem?",
        "Não sei se é amor ou egoísmo o que sinto, quero que ele fique mas também quero que acabe.",
    ]
    
    for i, inp in enumerate(test_cases, 1):
        response = agent.classify_emotion(inp)
        print(f"Teste {i}: {inp}")
        print(f"→ Emoção classificada: {response}\n")


def test_prompt_improver():
    agent=PromptImproverAgent()
    data=DataUtils("data/clinic_cases.csv")
    tests = [
    {
        "user_id": 1,
        "user_input": "Estou com dificuldades em alimentar a minha mãe.",
    },
    {
        "user_id": 2,
        "user_input": "Como posso ajudar minha mãe a lidar com dor intensa e alterações físicas?",
    },
    {
        "user_id": 3,
        "user_input": "Preciso de orientação para cuidados com a minha avó com PEG.",
    },
    {
        "user_id": 4,
        "user_input": "Meu pai está muito ansioso e não consegue dormir à noite. O que devo fazer?",
    }
]

    for test in tests:
        context = data.get_full_patient_info(test["user_id"])
        if context is None:
            print(f"Sem contexto para user_id {test['user_id']}")
            continue

        improved_prompt = agent.improve_prompt(
            text=test["user_input"],
            context={
                "name": context.get("patient_name"),
                "diseases": context.get("patient_diseases"),
                "description": context.get("patient_description")}
        )

        print(f"=== Test {test['user_id']} ===")
        print(f"Input: {test['user_input']}")
        print(f"Improved Prompt: {improved_prompt.content}\n")




async def testSummary():
    agent = SummarizeAgent(urlPath="https://www.sns.gov.pt/sns/cuidados-paliativos/", isUrl=True)
    splitDoc = agent.loadContent()

    print(f"[DEBUG] Total chunks ready for summarization: {len(splitDoc)}")
    
    app = agent.build_workflow()
    async for step in app.astream(
        {"contents": [doc.page_content for doc in splitDoc]},
        {"recursion_limit": 10},
    ):
        print(f"[DEBUG] Step keys: {list(step.keys())}")
        # Opcional: mostrar primeiro resumo de cada step
        if 'summaries' in step:
            print(f"[DEBUG] First summary snippet:\n{step['summaries'][0][:200]}")

        
def testInfoFetcher():
    agent = InfoFetcherAgent()

    # Carregar e dividir documentos
    docs = split_documentForEmbedding(
        "https://www.sns.gov.pt/sns/cuidados-paliativos/", isUrl=True
    )
    print(f"Loaded {len(docs)} chunks")

    agent.add_documents(docs)
    print("Documents added to vector store")

    # Consulta
    query = "O que são cuidados paliativos?"
    results = agent.retrieve(query, top_k=3)

    if results:
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:\n{doc.page_content[:500]}...\n")
    else:
        print("Nenhum resultado encontrado")


import asyncio

if __name__ == "__main__":
    url = "https://www.msdmanuals.com/pt/casa/fundamentos/morte-e-sofrimento/sintomas-durante-uma-doen%C3%A7a-fatal"
    docs = split_documentForEmbedding(url, isUrl=True)
    bot = ChatbotOrchestrator("data/clinic_cases.csv")
    
    # Executa a coroutine de forma correta
    asyncio.run(bot.chat_loop(user_id="5", theoretical_context=docs))
