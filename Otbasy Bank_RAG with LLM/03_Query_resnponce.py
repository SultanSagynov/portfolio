from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from colorama import Fore, Style, init
import os
import warnings


# Initialize colorama for color support
init(autoreset=True)

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Вы являетесь ассистентом, который помогает отвечать на вопросы, основываясь только на следующем контексте:

{context}

---

Ведите дружеский, разговорный диалог и отвечайте на вопросы пользователя на русском языке, основываясь на приведённом выше контексте: {question}
"""

def main():
    # Load OpenAI API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")
    
    # Prepare the DB
    embedding_function = OpenAIEmbeddings(openai_api_key=api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Initialize chat model
    model = ChatOpenAI(openai_api_key=api_key, max_tokens=500, temperature=0.7)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Start a conversation loop
    print(Fore.CYAN + "Добро пожаловать, я ваш ассистент в Отбасе банке, чем могу помочь? Для выхода с диалога наберите 'стоп'")
    context_memory = ""
    
    while True:
        query_text = input(Fore.YELLOW + "\nВаш Вопрос: ")
        if query_text.lower() == "стоп":
            print(Fore.CYAN + "До свидания!")
            break

        # Search the DB
        results = db.similarity_search_with_relevance_scores(query_text, k=5)
        
        # Ensure results meet a threshold of similarity score
        if len(results) == 0 or results[0][1] < 0.8:
            print(Fore.RED + "Ассистент: Я не смог найти нужную информацию в базе данных. Попробуйте перефразировать.")
            continue

        # Extract the context from the search results
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Include prior conversation context if available
        combined_context = f"{context_memory}\n\n{context_text}"
        
        # Create the prompt for the model
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=combined_context, question=query_text)
        
        # Generate response using the model
        response_text = model.predict(prompt)

        # Add response to the conversation context
        context_memory += f"\n\nВаш Вопрос: {query_text}\nАссистент:: {response_text}"
        
        # Retrieve sources for the response
        sources = [doc.metadata.get("source", None) for doc, _score in results]
        
        # Output the result with colors
        print(Fore.GREEN + f"Ассистент:: {response_text}")
        print(Fore.MAGENTA + f"(Источник: {sources})")

if __name__ == "__main__":
    main()