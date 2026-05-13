from fastapi import APIRouter

from app.services.chroma_service import collection
from app.services.gemini_service import generate_answer

router = APIRouter()


@router.get("/summary")
def generate_summary():

    results = collection.get()

    documents = results["documents"]

    context = "\n".join(documents[:15])

    question = """
    Summarize the uploaded document in detailed points.
    """

    answer = generate_answer(question, context)

    return {
        "summary": answer
    }