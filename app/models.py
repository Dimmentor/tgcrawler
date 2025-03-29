from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Source(Base):
    __tablename__ = 'sources'

    title: Mapped[str] = mapped_column(String, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    xpath: Mapped[str] = mapped_column(String, nullable=False)
