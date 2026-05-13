from fastapi import APIRouter
from pydantic import BaseModel

from app.services.video_recommendation import get_related_videos
from app.services.url_service import extract_text_from_url

from app.services.embedding_service import model
from app.services.chroma_service import search_similar_chunks
from app.services.gemini_service import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    url: str | None = None


@router.post("/chat")
def chat_with_pdf(data: ChatRequest):

    # CREATE QUESTION EMBEDDING
    query_embedding = model.encode(data.question).tolist()

    # SEARCH SIMILAR CHUNKS
    similar_chunks = search_similar_chunks(query_embedding)

    # CREATE CONTEXT
    context = "\n".join(similar_chunks)

    # EXTRACT WEBSITE TEXT IF URL PROVIDED
    if data.url:

        website_text = extract_text_from_url(data.url)

        context += "\n" + website_text

    # GENERATE AI ANSWER
    answer = generate_answer(data.question, context)

    # GET RELATED VIDEOS
    videos = get_related_videos(data.question)

    return {
        "question": data.question,
        "answer": answer,
        "context_used": similar_chunks,
        "related_videos": videos
    }