import asyncio
from sqlalchemy.dialects.postgresql import insert
from app.core.database import create_tables, SessionLocal
from app.models.tourist_place import TouristPlace
from app.repositories.mock_data import PLACES

async def main() -> None:
    await create_tables()
    async with SessionLocal() as session:
        for place in PLACES:
            statement = insert(TouristPlace).values(**place.model_dump()).on_conflict_do_nothing(index_elements=["id"])
            await session.execute(statement)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
