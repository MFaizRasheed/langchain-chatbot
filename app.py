from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature=0.7,
    # other params...
)

response = llm.invoke("What is Rag?")
print(response.content)