from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from db import Base

class DailyPuzzleCategory(Base):
    __table_args__ = (
        UniqueConstraint("puzzle_seed", "position"),
    )
    __tablename__ = "daily_puzzle_categories"

    puzzle_seed: Mapped[int] = mapped_column(
        ForeignKey("daily_puzzles.seed"),
        primary_key=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        primary_key=True
    )

    position: Mapped[int] = mapped_column(nullable=False)

    puzzle: Mapped["DailyPuzzle"] = relationship(
        back_populates="categories"
    )

    category: Mapped["Category"] = relationship(
        back_populates="puzzle_links"
    )
