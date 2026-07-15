from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/sample.pdf")
pages = loader.load()

for page in pages:
    print(page.page_content)