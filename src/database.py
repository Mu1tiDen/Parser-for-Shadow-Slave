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

def add_chapter_in_db(chapter_id: int | str, title: str, link: str | None = None, file_path: str | None = None):
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


def delete_chapter_by_id_from_db(id: int):
    with Session(engine) as session:
        chapter_n = session.get(Chapter, id)
        session.delete(chapter_n)
        session.commit()