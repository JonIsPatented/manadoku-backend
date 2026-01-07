from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from db import Base

class DailyPuzzle(Base):
    __tablename__ = "daily_puzzles"

    seed: Mapped[int] = mapped_column(primary_key=True)

    categories: Mapped[list["DailyPuzzleCategory"]] = relationship(
        back_populates="puzzle",
        cascade="all, delete-orphan",
        order_by="DailyPuzzleCategory.position",
    )
