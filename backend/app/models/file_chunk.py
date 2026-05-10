from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database.database import Base

class FileChunk(Base):
    __tablename__ = "file_chunks"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    module_id = Column(Integer, ForeignKey("modules.id"))
    chunk_text = Column(Text)