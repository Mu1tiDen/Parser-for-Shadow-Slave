from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

class Base(DeclarativeBase):
    pass

class Chapter(Base):
    __tablename__ = "Chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    chapter_id: Mapped[int]
    title: Mapped[str]
    link: Mapped[Optional[str]]
    file_path: Mapped[Optional[str]]

engine = create_engine("sqlite:///data/testdb.db", echo=False)

Base.metadata.create_all(engine)

def add_chapter_in_db(chapter_id: int | str, title: str, link: str | None = None, file_path: str | None = None) -> bool:
    try:
        with Session(engine) as session:
            chapter_n = Chapter(
                chapter_id=chapter_id,
                title=title,
                link=link,
                file_path=file_path,
            )
            session.add(chapter_n)
            session.commit()

            stmt = select(Chapter).where(Chapter.id.is_(chapter_n.id))

            for chapter_n in session.scalars(stmt):
                print(chapter_n.title)
        return True
    except:
        return False

def delete_chapter_by_id_from_db(id: int | str) -> bool:
    try:
        with Session(engine) as session:
            chapter_n = session.get(Chapter, id)
            session.delete(chapter_n)
            session.commit()
        return True
    except:
        return False

def is_something_in_db() -> bool:
    with Session(engine) as session:
        stmt = select(Chapter).where()
        chapters = session.scalars(stmt)
        if chapters.all():
            return True
        else: return False

def is_chapter_in_db(chapter_id: str | int) -> bool:
    with Session(engine) as session:
        stmt = select(Chapter).where(Chapter.chapter_id.is_(chapter_id))
        chapters = session.scalars(stmt)
        if chapters.all():
            return True
        else: return False
