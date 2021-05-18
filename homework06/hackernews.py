"""Bottle based hosting for classifier"""
from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, add_data, session, set_label
from scraputils import get_news

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///news.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_session(engine: Engine) -> Session:
    SessionLocal.configure(bind=engine)
    return SessionLocal()


@route("/")
@route("/news")
def news_list():
    """Show all news without labels"""
    rows = session().query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    """Mark news"""
    n_id = request.query["id"]
    n_label = request.query["label"]
    set_label(session(), n_id, n_label)
    redirect("/news")


@route("/update")
def update_news():
    """Expand database"""
    add_data(session(), get_news(url="https://news.ycombinator.com/newest", n_pages=4))
    redirect("/news")


colors = {"good": "#bdedbb", "never": "#ffd3bb", "maybe": "#e9eae6"}


@route("/classify")
def classify_news():
    """Show classified news list"""
    s = session()
    classifier = NaiveBayesClassifier()
    marked_data = s.query(News).filter(News.label is not None).all()
    classifier.fit([row.title for row in marked_data], [row.label for row in marked_data])
    news = s.query(News).filter(News.label is None).all()
    data = []
    for row in news:
        data.append(row.title)
    for i, row in enumerate(classifier.predict(data)):
        data[i] = colors[row]
    colored_data = sorted(zip(data, news), key=lambda tup: tup[0])
    print(colored_data)
    return template("color_template", rows=colored_data)


if __name__ == "__main__":
    run(host="localhost", port=8080)
