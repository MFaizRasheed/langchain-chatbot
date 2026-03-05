from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage#,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature = 0.7,
    #other parameters
)

promt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful AI assistant. "),
    ("human","{question}")
])
chain = promt | llm | StrOutputParser()
# response = chain.invoke({"question":"What is RAG?"})
# print(response)
for chunk in chain.stream({"question":"What is RAG?"}):
    print(chunk, end="", flush=True)