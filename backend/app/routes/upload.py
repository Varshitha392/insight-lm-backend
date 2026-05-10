import os
import shutil

from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.file import File
from app.models.module import Module
from app.models.user import User

from app.utils.auth import get_current_user

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_splitter import split_text

from app.services.embedding_service import generate_embeddings
from app.services.chroma_service import store_embeddings

router = APIRouter()

UPLOAD_FOLDER = "uploads"


@router.post("/upload/{module_id}")
def upload_file(
    module_id: int,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    module = db.query(Module).filter(
        Module.id == module_id,
        Module.user_id == current_user.id
    ).first()

    if not module:
        return {"message": "Module not found"}

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = File(
        filename=file.filename,
        filepath=file_location,
        module_id=module.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    extracted_text = ""
    chunks = []
    embeddings = []

    if file.filename.endswith(".pdf"):

        extracted_text = extract_text_from_pdf(file_location)

        chunks = split_text(extracted_text)

        embeddings = generate_embeddings(chunks)

        store_embeddings(chunks, embeddings)

    return {
        "message": "File uploaded successfully",
        "file_id": new_file.id,
        "filename": new_file.filename,
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "sample_chunk": chunks[0] if chunks else ""
    }