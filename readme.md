# Paliative care chat bot Prototype:
## Abstract:
- The main goal of this project is to develop a prototype of a chatbot designed to support family members and informal caregivers when palliative care professionals are not available to provide assistance.

- To train and inform the chatbot, we will use clinical case studies, general knowledge about palliative care, and specific information about the patient being cared for by the family or informal caregiver. The quality and reliability of these information sources are crucial to ensure accurate and meaningful responses, and to minimize the risk of hallucinations (i.e., the model generating false or unsupported information).

## Agent Workflow

- **Prompt Improver Agent**  
  This agent is responsible for improving the user’s prompt to ensure that the input is clear, concise, and free of redundant information. Its goal is to make the queries more consistent so that the chatbot can generate better responses.

- **Emotion Interpreter Agent**  
  This agent analyzes the user’s emotion, context, and level of distress. Depending on the situation, the chatbot’s response style changes:  
    - In stressful situations, the chatbot should provide information **as clearly and directly as possible**, without unnecessary explanations.  
    - In calm situations, the chatbot can provide more detailed and informative responses.

- **Knowledge Agent**  
  This agent summarizes and indexes all background information, providing a **scientific and evidence-based foundation** for the chatbot. It organizes:  
  - Generic palliative care knowledge  
  - Patient-specific information

- **ChatBot Agent**  
  This agent receives the improved prompt, the emotional context, and the relevant knowledge from the Knowledge Agent to generate **precise and helpful responses**, adapting to the user’s emotional and situational context.

![Diagrama](images/agentDiagramV1.png)


### Adition agents (future work)
- **Feedback Agent**  
  This agent is responsible for **evaluating the chatbot’s output**. It checks whether the generated response is appropriate, accurate, and helpful, providing feedback to improve or refine the final output if necessary.
