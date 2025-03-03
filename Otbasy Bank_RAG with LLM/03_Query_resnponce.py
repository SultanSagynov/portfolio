from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from colorama import Fore, Style, init
import os
import warnings


init(autoreset=True)

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
    
    embedding_function = OpenAIEmbeddings(openai_api_key=api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    model = ChatOpenAI(openai_api_key=api_key, max_tokens=500, temperature=0.7)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print(Fore.CYAN + "Добро пожаловать, я ваш ассистент в Отбасе банке, чем могу помочь? Для выхода с диалога наберите 'стоп'")
    context_memory = ""
    
    while True:
        query_text = input(Fore.YELLOW + "\nВаш Вопрос: ")
        if query_text.lower() == "стоп":
            print(Fore.CYAN + "До свидания!")
            break

        results = db.similarity_search_with_relevance_scores(query_text, k=5)
        
        if len(results) == 0 or results[0][1] < 0.8:
            print(Fore.RED + "Ассистент: Я не смог найти нужную информацию в базе данных. Попробуйте перефразировать.")
            continue

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        combined_context = f"{context_memory}\n\n{context_text}"
        
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=combined_context, question=query_text)
        
        response_text = model.predict(prompt)

        context_memory += f"\n\nВаш Вопрос: {query_text}\nАссистент:: {response_text}"
        
        # Retrieve sources for the response
        sources = [doc.metadata.get("source", None) for doc, _score in results]
        
        print(Fore.GREEN + f"Ассистент:: {response_text}")
        print(Fore.MAGENTA + f"(Источник: {sources})")

if __name__ == "__main__":
    main()
