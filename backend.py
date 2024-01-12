import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = os.getenv("OpenAI_Key")

class Backend:
    def __init__(self):
        self.vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
        self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

        self.model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) # temperature controls amount of randomness, 0: deterministic, 1: wild variation

        self.template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Context: {context}
        Question: {question}
        Helpful Answer:"""
        self.prompt_custom = PromptTemplate.from_template(self.template)

        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()} # retriever is a Runnable object
            | self.prompt_custom
            | self.model
            | StrOutputParser()
        )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_response(self, query):
        # for chunk in rag_chain.stream(query): # query gets passed via RunnablePassthrough() above
        #     print(chunk, end="", flush=True)  # stream response during execution
        # print('')

        return self.rag_chain.invoke(query) # wait for completion then provide response