from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

CHROMA_PATH = "chroma_db"

SYSTEM_PROMPT = """Ти — Garden Auntie, дружня та знаюча помічниця з садівництва.
Ти відповідаєш українською мовою, тепло і практично, як досвідчена сусідка-садівниця.

Використовуй наданий контекст як основне джерело інформації.
Якщо питання стосується ігор (наприклад, Stardew Valley), відповідай відповідно до ігрового контексту.
Якщо інформації в контексті недостатньо, можеш доповнити загальними знаннями, але спочатку спирайся на контекст.
Якщо не знаєш відповіді — так і скажи чесно.

Контекст:
{context}"""


def get_answer(question: str, k: int = 4) -> dict:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.invoke(question)

    context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
    sources = [doc.metadata.get("source", "unknown") for doc in relevant_docs]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(context=context)),
        HumanMessage(content=question),
    ]

    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "sources": list(set(sources)),
    }


if __name__ == "__main__":
    print("Garden Auntie — тестовий режим")
    print("Введи 'вихід' щоб завершити\n")

    while True:
        question = input("Твоє питання: ").strip()
        if question.lower() in ("вихід", "exit", "quit"):
            break
        if not question:
            continue

        result = get_answer(question)
        print(f"\nВідповідь:\n{result['answer']}")
        print(f"\nДжерела: {', '.join(result['sources'])}\n")
        print("-" * 50)
