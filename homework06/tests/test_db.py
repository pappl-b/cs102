from sqlalchemy.engine import create_engine
import db
import pytest

test_news = [
    {"title": "Elon Musk died", "url": "oh.no", "points": 200, "author": "Shiza"},
    {
        "title": "Restructurisation is declined",
        "url": "itmo.ru",
        "points": 13,
        "author": "ITMO",
    },
]

def db_set_up(engine):
    db.Base.metadata.create_all(bind=engine)

def db_tear_down(session):
    session.query(db.News).delete()
    session.commit()
    session.close()


@pytest.fixture
def engine():
    return create_engine("sqlite://")

@pytest.fixture
def session(engine):
    session = db.get_session(engine)
    db_set_up(engine)
    yield session
    db_tear_down(session)


def test_news_can_be_saved(session):
    db.get_new_news(session=session, news=test_news)

    saved_item = session.query(db.News).get(1)
    assert saved_item.title == test_news[0]["title"]
    assert saved_item.author == test_news[0]["author"]

    saved_item = session.query(db.News).get(2)
    assert saved_item.title == test_news[1]["title"]
    assert saved_item.author == test_news[1]["author"]


def test_can_news_be_labeled(session):
    db.get_new_news(session=session, news=test_news)

    saved_item = session.query(db.News).get(1)
    assert saved_item.label is None

    label = "good"
    db.set_label(session=session, id=1, label=label)
    saved_item = session.query(db.News).get(1)
    assert saved_item.label == label