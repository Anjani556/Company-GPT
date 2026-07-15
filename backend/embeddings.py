from langchain_ollama import OllamaEmbeddings

# Ollama embeddings model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Test cheddam
text = ["Hello world", "This is a test"]
result = embeddings.embed_documents(text)

print("Embedding vector length:", len(result[0]))
print("Done ✅")