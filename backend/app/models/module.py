from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="modules")