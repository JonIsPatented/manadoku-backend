from itertools import combinations
from typing import Iterable
import random
from sqlalchemy.orm import Session
import scrython
from models import Category

def generate_daily_puzzle(
    session: Session,
    seed: int,
) -> list[Category]:
    rng = random.Random(seed)

    categories = session.query(Category).all()

    if len(categories) < 6:
        raise ValueError("Not enough categories")

    rng.shuffle(categories)
    
    non_type_categories = [category for category in categories if not category.filter.startswith("t:") and " t:" not in category.filter]

    if len(non_type_categories) < 3:
        raise ValueError("Not enough non-type categories")

    types_on_columns = rng.choice([True, False])

    for rows, cols in generate_puzzle_candidates(categories, non_type_categories, types_on_columns):
        if is_valid_puzzle(rows, cols):
            return rows + cols

    return rng.sample(non_type_categories, 6)

def generate_puzzle_candidates(
    categories: list[Category],
    non_type_categories: list[Category],
    types_on_columns: bool,
) -> Iterable[tuple[list[Category], list[Category]]]:
    if types_on_columns:
        for rows in combinations(non_type_categories, 3):
            for cols in combinations(categories, 3):
                yield list(rows), list(cols)
    else:
        for cols in combinations(non_type_categories, 3):
            for rows in combinations(categories, 3):
                yield list(rows), list(cols)

def is_valid_puzzle(
    rows: list[Category],
    columns: list[Category],
) -> bool:
    for row in rows:
        for col in columns:
            if row.id == col.id:
                return False
            if not is_solvable_cell(row, col):
                return False
    return True

def is_solvable_cell(
    row: Category,
    column: Category,
) -> bool:
    query = f"game:paper not:extras {row.filter} {column.filter}"

    try:
        cards = scrython.cards.Search(
            q=query,
            unique="cards",
            order="name",
        )

        return cards.total_cards >= 8

    except Exception as e:
        print(f"Scryfall error for query '{query}': {e}")
        return False
