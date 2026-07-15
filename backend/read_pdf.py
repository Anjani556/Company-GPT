from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader("data")
documents = loader.load()

for doc in documents:
    print("=" * 50)
    print(doc.page_content)