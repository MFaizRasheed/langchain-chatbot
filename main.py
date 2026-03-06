from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()

max_turn = os.getenv("MAX_TURNS")
MODEL_NAME = os.getenv("MODEL_NAME", "minimax-m2.5:cloud")
TEMPERATURE = os.getenv("TEMPERATURE", 0.7)

# LLM
llm = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

# Chain
chain = prompt | llm | StrOutputParser()

# Conversation memory
chat_history = []
max_turn = 5  # number of conversation turns


def chat(question):
    current_turns = len(chat_history) // 2

    if current_turns >= max_turn:
        return (
            "Context window is full. "
            "The AI may not follow your previous thread properly. "
            "Please type 'clear' for a new chat."
        )

    # invoke LLM
    try:
        response = chain.invoke({"question": question, "chat_history": chat_history})
    except Exception as e:
        print("Error: ", e)
    # store conversation
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))

    remaining = max_turn - (current_turns + 1)

    if remaining <= 2:
        response += f"\n\n⚠️ {remaining} turn(s) left before memory resets."

    return response


def main():
    print("LangChain Chatbot Ready! (Type 'quit' to exit, 'clear' to reset history)")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            chat_history.clear()
            print("History cleared!")
            continue

        # generate response
        response = chat(user_input)

        print("AI:", response)


main()
