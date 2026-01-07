from sqlalchemy.orm import Session
from models import DailyPuzzle, DailyPuzzleCategory
from services.puzzle_generator import generate_daily_puzzle

def get_or_create_daily_puzzle(
    session: Session,
    seed: int,
) -> DailyPuzzle:

    puzzle = session.get(DailyPuzzle, seed)
    if puzzle:
        return puzzle

    # Generate new puzzle
    categories = generate_daily_puzzle(session, seed)

    puzzle = DailyPuzzle(seed=seed)
    session.add(puzzle)

    for index, category in enumerate(categories):
        link = DailyPuzzleCategory(
            puzzle_seed=seed,
            category_id=category.id,
            position=index,
        )
        session.add(link)

    session.commit()
    session.refresh(puzzle)

    return puzzle

