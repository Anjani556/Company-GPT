from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFDirectoryLoader("data")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print("Total chunks:", len(chunks))
for chunk in chunks:
    print("=" * 50)
    print(chunk.page_content)