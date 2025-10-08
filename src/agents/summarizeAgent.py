from models.llm_factory import get_google_genai
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from typing import  List,Literal
from memory.summaryStates import OverallState, SummaryState
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
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

        self.map_prompt  = ChatPromptTemplate.from_messages(
        
        [("system", "Write a concise summary of the following:\\n\\n{context}")])
        
        reduce_template = """
                The following is a set of summaries:
                {docs}
                Take these and distill it into a final, consolidated summary
                of the main themes.
            """
        self.reduce_prompt = reduce_prompt = ChatPromptTemplate([("human", reduce_template)])

    def length_function(self,documents: List[Document]) -> int:
        """Get number of tokens for input contents."""
        return sum(self.model.get_num_tokens(doc.page_content) for doc in documents)

    async def generate_summary(self, state: SummaryState):
        
        if not state.get("content"):
            raise ValueError("state['content'] não está definido ou está vazio")
        
      
        prompt = self.map_prompt.invoke({"context": state["content"]})
        response = await self.model.ainvoke(prompt)
        return {"summaries": [response.content]}


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
    async def _reduce(self,input: dict) -> str:
        prompt = self.reduce_prompt.invoke(input)
        response = await self.model.ainvoke(prompt)
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

    def loadContent(self):
        if self.isUrl:
            loader = WebBaseLoader(self.urlPath)
            docs = loader.load()
            
        else:
            loader = PyPDFLoader(self.urlPath)
            docs = loader.load()
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents(docs)
        return split_docs

# TODO