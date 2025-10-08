from agents.chatBotAgent import ChatBotAgent
from agents.emotionalStateAgent import EmotionalStateAgent
from agents.infoFetcher import InfoFetcherAgent
from agents.promptImproverAgent import PromptImproverAgent
from agents.summarizeAgent import SummarizeAgent
from utils.docs_utils import split_documentForEmbedding
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


def testPromptImprover():
     #testChatBot()
    user_prompts = [
   
    "Não aguento mais ver a minha mãe assim, todos os dias piora e eu não sei o que fazer...",

    "O que posso fazer para aliviar a dor do meu pai em casa?",
   

    "A minha mãe não quer continuar o tratamento, devo respeitar a decisão dela?",
 

    "Sinto-me sozinho, ninguém parece compreender o que estou a passar.",
   
  
    "A médica disse que talvez seja melhor parar o tratamento, mas não percebi bem o que isso implica.",

  
    "Existem grupos de apoio para familiares de doentes em cuidados paliativos?",
    
]
    agent = PromptImproverAgent()
    for i, prompt in enumerate(user_prompts, 1):
        improved = agent.improve_prompt(prompt)
        print(f"Teste {i}:")
        print(f"Prompt original: {prompt}")
        print(f"Prompt   melhorado: {improved}\n")

 



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


if __name__ == "__main__":
    #testChatBot()
    #testEmotionBot()
    #testPromptImprover()
    #import asyncio
    #asyncio.run(testSummary())
    testInfoFetcher()