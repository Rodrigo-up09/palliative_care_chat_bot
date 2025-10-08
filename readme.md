# Paliative care chat bot Prototype:
## Abstract:
- The main goal of this project is to develop a prototype of a chatbot designed to support family members and informal caregivers when palliative care professionals are not available to provide assistance.

- To train and inform the chatbot, we will use clinical case studies, general knowledge about palliative care, and specific information about the patient being cared for by the family or informal caregiver. The quality and reliability of these information sources are crucial to ensure accurate and meaningful responses, and to minimize the risk of hallucinations (i.e., the model generating false or unsupported information).

## Agent Workflow

- ## Prompt Improver Agent
  This agent is responsible for improving the user’s prompt to ensure that the input is clear, concise, and free of redundant information. Its goal is to make the queries more consistent so that the chatbot can generate better responses.

  ### Results:

  | Test | Input | Improved Prompt |
  |------|-------|----------------|
  | 1 | Estou com dificuldades em alimentar a minha mãe. | Estou com dificuldades em alimentar a minha mãe, D. Antónia, de 82 anos. Ela tem uma PEG para alimentação devido à maxilectomia e traqueostomia recentes, e está muito assustada com a sua nova condição clínica. Como posso gerir melhor o processo de alimentação, considerando estas dificuldades e o seu estado emocional? |
  | 2 | Como posso ajudar minha mãe a lidar com dor intensa e alterações físicas? | Como posso, como filha(o), auxiliar minha mãe, Joana, a gerir a dor intensa das suas cefaleias e as alterações físicas decorrentes do glioblastoma, como as alterações sensoriais na hemiface direita, zumbidos e visão dupla, que a afetam diariamente e contribuem para o seu medo e ansiedade? |
  | 3 | Preciso de orientação para cuidados com a minha avó com PEG. | Como neta de D. Antónia, a minha avó de 82 anos que tem uma sonda PEG desde outubro, preciso de orientação prática sobre os cuidados diários. Ela está cognitivamente íntegra, mas muito assustada com a sua nova condição. Gostaria de saber como gerir a higiene da PEG, a administração segura de alimentação e medicação, e como posso apoiá-la emocionalmente para lidar com o desconforto e o medo. |
  | 4 | Meu pai está muito ansioso e não consegue dormir à noite. O que devo fazer? | Meu pai, Sr. Nuno, de 76 anos, que sofre de carcinoma de pequenas células do pulmão estadio IV, metástase cerebral provável e óssea, e que se encontra com degradação do estado geral, dependente no autocuidado e caquexia, está muito ansioso e não consegue dormir à noite. Atualmente a receber Imipenem e Vancomicina devido a sépsis, o que devo fazer para o ajudar com a ansiedade e a insónia? |

- ## Emotion Interpreter Agent

  ### Purpose
  This agent analyzes the user's **emotion**, **context**, and **level of distress**.  
  Depending on the emotional state, the chatbot dynamically adapts its **response style**:

  - **Stressful situations (high distress):**  
    The chatbot should respond **clearly and directly**, avoiding long or complex explanations.  
  - **Calm situations (low distress):**  
    The chatbot can offer **more detailed and informative** responses.

  ---

  ### Context Prompt
  Represents the family's **emotional intensity or level of distress** on a scale from **1 to 10**:

  | Level | Description | Chatbot Behavior |
  |:------:|--------------|------------------|
  | **1–3** | Calm or curious — the family is simply seeking information. | Provide friendly, detailed, and educational answers. |
  | **4–7** | Concerned or anxious — the family needs reassurance and clear guidance. | Be concise but empathetic, offering clear next steps. |
  | **8–10** | Urgent or desperate — the family is emotionally overwhelmed. | Provide short, direct, and comforting responses. |

  ---

  ### Usage Examples
  | Test | Input Sentence | Classified Emotion (1–10) | Interpretation |
  |:----:|----------------|:--------------------------:|----------------|
  | **1** | _"Sinto-me muito em baixo, a saúde da minha mãe piorou."_ | **9** | Deep sadness and despair; needs emotional support. |
  | **2** | _"Estou um pouco preocupado com a situação, mas acho que vai correr tudo bem."_ | **5** | Moderate concern with optimism; balanced tone. |
  | **3** | _"Estou preocupado com a dor que a minha mãe está a sentir."_ | **6** | Noticeable distress; seeking reassurance. |
  | **4** | _"Porque é que nada parece funcionar direito aqui?"_ | **9** | High frustration and emotional tension. |
  | **5** | _"Bom dia, gostaria de saber o estado clínico da minha mãe."_ | **2** | Calm, neutral inquiry; low emotional intensity. |
  | **6** | _"Estou um pouco preocupado, a minha mãe não tem comido bem."_ | **6** | Mild to moderate concern. |
  | **7** | _"Ela parece pior hoje, mas talvez seja só cansaço."_ | **6** | Concern mixed with cautious optimism. |
  | **8** | _"Já não sei o que fazer, isto tem sido muito difícil."_ | **9** | Emotional exhaustion and helplessness. |

  ---

- ## Summarize Agent
  - Not used in the MVP

  **Summarize Agent**  
  This agent is responsible for **summarizing and condensing multiple sources of information** into clear, concise summaries. It provides a **scientific and structured foundation** for downstream agents in the chatbot workflow. Key features include:

  - Aggregates and condenses content from multiple documents or web sources.
  - Uses a **map-reduce approach** to handle large amounts of information efficiently.
  - Generates intermediate summaries and a final consolidated summary.
  - Ensures that the summaries stay **faithful to the original content** and do not invent information.
  - Can be configured to summarize content from URLs, defaulting to trusted palliative care sources if no URL is provided.
  - Integrates seamlessly with the overall chatbot architecture, supporting patient-specific and general knowledge aggregation.

- ## InfoFetcher Agent

  **InfoFetcher Agent**  
  This agent is responsible for **retrieving the most relevant information** to answer user queries. It provides a **document-based evidence layer** for the chatbot, ensuring responses are grounded in available knowledge. Key features include:

  - Stores documents in a **vector database** using embeddings.
  - Performs **similarity search** to find the most relevant content for a given query.
  - Supports dynamic addition of new documents at runtime.
  - Ensures that the chatbot can base its answers on **retrieved, contextually relevant sources**, rather than guessing.
  - Integrates with the summarization and chat agents to provide **theoretical context** for responses.


- ## ChatBot Agent
  This agent receives the improved prompt, the emotional context, and the relevant knowledge from the Knowledge Agent to generate **precise and helpful responses**, adapting to the user’s emotional and situational context.
    ### Context Prompt
     ```python
      system",
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
      "Emotional context: {emotional_context}\n"
      ),
      MessagesPlaceholder(variable_name="messages"),
      ])
  ```



## Chatbot Orchestrator Workflow

**Chatbot Orchestrator**  
This orchestrator coordinates all the agents involved in the palliative care chatbot, providing a **seamless workflow** from user input to response generation. The workflow is as follows:

1. **User Input**
   - The family member or caregiver inputs a question or concern about the patient.

2. **Patient Context Retrieval**
   - The orchestrator fetches full patient information from the database (`DataUtils`) based on `user_id`.

3. **Prompt Improvement**
   - The `PromptImproverAgent` refines the user's raw input, integrating patient-specific context for a more precise query.

4. **Emotion Classification**
   - The `EmotionalStateAgent` analyzes the user input to determine the emotional context (stress/anxiety level).

5. **Document Retrieval**
   - The `InfoFetcherAgent` adds theoretical context documents and retrieves the **most relevant documents** based on the improved prompt.

6. **Response Generation**
   - The `ChatBotAgent` generates a response using:
     - The improved prompt
     - Retrieved documents
     - Emotional context
     - Patient-specific information

7. **Output**
   - The chatbot outputs a **contextual, evidence-based, and emotionally adjusted response** to the user.

8. **Interactive Loop**
   - The `chat_loop` method continues to process inputs until the user types "sair"/"exit"/"quit", allowing a real-time conversational simulation.

**Note:**  
This orchestrator ensures that the chatbot remains **scientifically grounded**, adapts to **user emotions**, and integrates **patient-specific details** to provide practical and empathetic guidance in palliative care scenarios.


![Diagrama](images/agentDiagramV1.png)

### Additional Agents (Future Work)

- **Feedback Agent**  
  Responsible for **evaluating the chatbot’s output**. It would check if the generated response is appropriate, accurate, and helpful, providing feedback to improve or refine the final output when necessary.

- **Message Pruning**  
  Messages are currently stored in the `ChatBotAgent`, which could lead to buffer overflow over time. Implementing an algorithm to prune messages while preserving important information is needed.

- **Summarized Agent**  
  Although a summarization agent is implemented, it is currently unused. Since this project does not work with a large information source, it was not necessary. However, a workflow connecting `InfoFetcherAgent` and the `SummarizeAgent` could improve performance for larger datasets.

- **RailGuard Agent**  
  Intended to **keep the chatbot within context** and protect it from potential external attacks or malicious input.

- **Database Integration**  
  The current system uses a simple CSV file for storing patient information. For scalability, a proper database solution should be implemented.

## Notes

- This project is a **prototype**. The knowledge base of the model is minimal, relying only on a random webpage about palliative care.
- The **search results are basic** since they rely on a simple similarity search and should be improved for better accuracy.
- Prompts are based on **ChatGPT-style instructions** because this project is not created by a palliative care specialist—just someone interested in agents and AI.
- There is **no frontend**, which makes it less interactive and harder to visualize the workflow.
- **Important:** This is a conceptual prototype. The basic workflow is established, but the results are preliminary and should not be used in real clinical settings.
