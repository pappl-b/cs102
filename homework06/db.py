"""Create local database using sqlalchemy"""
import typing as tp

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from scraputils import get_news

"""Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)"""

Base = declarative_base()
path_news_db = "sqlite:///news.db"
engine = create_engine(path_news_db, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False)


class News(Base):  # type: ignore
    """Database entity"""

    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


@tp.no_type_check
def get_session(engine: Engine) -> Session:
    local_session.configure(bind=engine)
    return local_session()


def add_data(_session: Session, data: tp.List[tp.Dict[str, tp.Union[int, str]]]) -> None:
    """Write unique rows to the database"""
    for item in data:
        if not list(
            _session.query(News).filter(News.author == item["author"], News.title == item["title"])
        ):
            row = News(
                title=item["title"],
                author=item["author"],
                url=item["url"],
                points=item["points"],
                comments=item["comments"],
            )
            _session.add(row)
    _session.commit()


@tp.no_type_check
def set_label(session: Session, row_id: int, label: str) -> None:
    item = session.query(News).get(row_id)
    item.label = label
    session.commit()


def get_new_news(session: Session, url: str = "https://news.ycombinator.com/newest") -> None:
    news = get_news(url)
    news_news = []
    for something in news:
        main, name = something["title"], something["author"]
        if not list(session.query(News).filter(News.title == main, News.author == name)):
            news_news.append(something)
    add_data(session, news_news)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    add_data(get_session(engine), get_news(url="https://news.ycombinator.com/newest", n_pages=4))
