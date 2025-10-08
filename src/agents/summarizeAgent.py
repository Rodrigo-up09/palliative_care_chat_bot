from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate
from typing import  List,Literal
from memory.summaryStates import OverallState, SummaryState
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage

# method used Map-reduce
# source https://python.langchain.com/docs/tutorials/summarization/
class SummarizeAgent:

    def __init__(self,tokens_max=1000,urlPath="",isUrl=True):
        self.tokens_max=tokens_max
        self.model = get_google_genai()
        if(urlPath==""):
            self.urlPath="https://www.sns.gov.pt/sns/cuidados-paliativos/" #default url

        self.urlPath=urlPath
        self.isUrl=isUrl
        



    def length_function(self,documents: List[Document]) -> int:
        """Get number of tokens for input contents."""
        return sum(self.model.get_num_tokens(doc.page_content) for doc in documents)

    async def generate_summary(self, state: SummaryState):
        # Cria prompt para resumir o conteúdo original
        message = HumanMessage(content=f"Write a concise summary of the following:\n\n{state['content']}")
        response = await self.model.ainvoke([message])
        print(f"[DEBUG] Summary response length: {len(response.content)}")
        return {"summaries": [response.content]}  # devolve num dicionário

    def map_summaries(self,state: OverallState):
        # We will return a list of `Send` objects
        # Each `Send` object consists of the name of a node in the graph
        # as well as the state to send to that node
        return [
            Send("generate_summary", {"content": content}) for content in state["contents"]
        ]

    def collect_summaries(self,state: OverallState):
        return {
            "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
        }
    
    async def _reduce(self, input: list) -> str:
        # Garante que estamos a juntar o conteúdo textual de cada documento
        summaries_text = "\n\n".join(
            doc.page_content if isinstance(doc, Document) else str(doc)
            for doc in input
        )

        message = HumanMessage(
            content=(
                "Take the following summaries and distill them into a final, "
                "consolidated summary of the main themes:\n\n"
                f"{summaries_text}"
            )
        )

        response = await self.model.ainvoke([message])
        print(f"[DEBUG] Reduce response length: {len(response.content)}")
        return response.content

    
    async def collapse_summaries(self,state: OverallState):
        doc_lists = split_list_of_docs(
            state["collapsed_summaries"], self.length_function, self.tokens_max
        )
        results = []
        for doc_list in doc_lists:
            results.append(await acollapse_docs(doc_list, self._reduce))

        return {"collapsed_summaries": results}
        # This represents a conditional edge in the graph that determines
    # if we should collapse the summaries or not

    def should_collapse(self,
        state: OverallState,
    ) -> Literal["collapse_summaries", "generate_final_summary"]:
        num_tokens = self.length_function(state["collapsed_summaries"])
        if num_tokens > self.tokens_max:
            return "collapse_summaries"
        else:
            return "generate_final_summary"
        
    # Here we will generate the final summary
    async def generate_final_summary(self, state: OverallState):
        response = await self._reduce(state["collapsed_summaries"])
        return {"final_summary": response}


    def build_workflow(self) -> StateGraph:
        graph = StateGraph(OverallState)
        graph.add_node("generate_summary", self.generate_summary)  
        graph.add_node("collect_summaries", self.collect_summaries)
        graph.add_node("collapse_summaries", self.collapse_summaries)
        graph.add_node("generate_final_summary", self.generate_final_summary)

        # Edges:
        graph.add_conditional_edges(START, self.map_summaries, ["generate_summary"])
        graph.add_edge("generate_summary", "collect_summaries")
        graph.add_conditional_edges("collect_summaries", self.should_collapse)
        graph.add_conditional_edges("collapse_summaries", self.should_collapse)
        graph.add_edge("generate_final_summary", END)
        app = graph.compile()
        return app

    

