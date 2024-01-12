import os
import requests

import bs4
from bs4 import BeautifulSoup

from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.text_splitter import RecursiveCharacterTextSplitter

os.environ["OPENAI_API_KEY"] = os.getenv("OpenAI_Key")

r = requests.get("https://community.canvaslms.com/t5/Student-Guide/tkb-p/student")
html = r.content

soup = BeautifulSoup(html, "html.parser")

toc_main = soup.find("div", attrs = {"class":"toc-main"})
anchors = toc_main.find_all("a")

urls = []

for anchor in anchors:
  urls.append("https://community.canvaslms.com" + anchor["href"])

loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs={ # beautiful soup key word arguments
        "parse_only": bs4.SoupStrainer(class_=("MessageSubject", "lia-message-body-content")) # class selectors
    },
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = text_splitter.split_documents(docs)

print(f"{len(all_splits)} total chunks")
for split in all_splits[:5]:
    print(split.metadata)

vectorstore1 = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")