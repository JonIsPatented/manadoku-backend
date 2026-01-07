from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from db import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    summary: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    filter: Mapped[str] = mapped_column(String, nullable=False)
    
    puzzle_links: Mapped[list["DailyPuzzleCategory"]] = relationship(
        back_populates="category"
    )
