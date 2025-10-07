from agents.chatBotAgent import ChatBotAgent
from agents.emotionalStateAgent import EmotionalStateAgent

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
        "Sinto-me muito em baixo, a saúde da minha mãe piorou.",
        "Estou um pouco preocupado com a situação, mas acho que vai correr tudo bem.",
        "Estou preocupado com a dor que a minha mãe está a sentir.",
        "Porque é que nada parece funcionar direito aqui?",
        "Bom dia, gostaria de saber o estado clínico da minha mãe.",
        "Estou um pouco preocupado, a minha mãe não tem comido bem.",
        "Ela parece pior hoje, mas talvez seja só cansaço.",
        "Já não sei o que fazer, isto tem sido muito difícil."


    ]
    
    for i, inp in enumerate(test_cases, 1):
        response = agent.classify_emotion(inp)
        print(f"Teste {i}: {inp}")
        print(f"→ Emoção classificada: {response}\n")


if __name__ == "__main__":
    #testChatBot()
    testEmotionBot()