from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def clean_html_documents(docs: list[Document]) -> list[Document]:
    cleaned_docs = []
    for doc in docs:
        soup = BeautifulSoup(doc.page_content, "html.parser")
        text = soup.get_text(separator="\n")  # mantém quebras de linha
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])  # remove linhas vazias
        cleaned_docs.append(Document(page_content=text, metadata=doc.metadata))
    return cleaned_docs


def split_documentForSummarization(docPath: str, isUrl: bool = False):
        if isUrl:
            loader = WebBaseLoader(docPath)
            docs = loader.load()
            
        else:
            loader = PyPDFLoader(docPath)
            docs = loader.load()
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents(docs)
        return split_docs

def split_documentForEmbedding(docPath: str, isUrl: bool = False):
    if isUrl:
        loader = WebBaseLoader(docPath)
        docs = loader.load()
    else:
        loader = PyPDFLoader(docPath)
        docs = loader.load()

    # Limpar HTML
    docs = clean_html_documents(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits
