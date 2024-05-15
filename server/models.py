from sqlalchemy import Column, Integer, String
from database.connection import Base
from pydantic import BaseModel


class Url(Base):
    address = Column(String, unique=True)
    code = Column(Integer)
    verdict = Column(String)
    phishing = Column(Integer)
    legitimate = Column(Integer)

    def __repr__(self):
        return f"<User {self.url}>"


def UrlResponseDTO(BaseModel):
    address: str
    code: int
    verdict: str
    phishing: int
    legitimate: int
