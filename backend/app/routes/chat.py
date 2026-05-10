from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import model
from app.services.chroma_service import search_similar_chunks
from app.services.gemini_service import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat_with_pdf(data: ChatRequest):

    query_embedding = model.encode(data.question).tolist()

    similar_chunks = search_similar_chunks(query_embedding)

    context = "\n".join(similar_chunks)

    answer = generate_answer(data.question, context)

    return {
        "question": data.question,
        "answer": answer,
        "context_used": similar_chunks
    }