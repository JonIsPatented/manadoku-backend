from db import SessionLocal
from models import Category
from seed_data.categories import CATEGORIES

def seed_categories():
    session = SessionLocal()

    try:
        for data in CATEGORIES:
            exists = session.query(Category).filter_by(
                filter=data["filter"]
            ).first()

            if exists:
                continue

            category = Category(**data)
            session.add(category)

        session.commit()
        print("Categories seeded successfully")

    except Exception as e:
        session.rollback()
        print("Error seeding categories:", e)

    finally:
        session.close()

if __name__ == "__main__":
    seed_categories()

