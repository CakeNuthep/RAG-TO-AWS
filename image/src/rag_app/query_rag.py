from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from rag_app.get_chroma_db import get_chroma_db

PROMPT_TEMPLATE = """
คุณเป็นตัวแทนคนที่ชื่อว่าเค้ก ะป็นเพศชาย สามารถตอบคำถามเป็นภาษาไทยได้จากบทความข้างล่าง:

{context}

---

สามารถตอบคำถามเป็นภาษาไทยได้จากบทความด้านบน:
คำถามคือ {question}
"""

BEDROCK_MODEL_ID = "meta.llama3-70b-instruct-v1:0"


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]


def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
    response = model.invoke(prompt)
    response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


if __name__ == "__main__":
    query_rag("How much does a landing page cost to develop?")
