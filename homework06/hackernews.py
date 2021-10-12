"""Bottle based hosting for classifier"""
import typing as tp

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, add_data, engine, get_session, set_label
from scraputils import get_news


@tp.no_type_check
@route("/")
@route("/news")
def news_list() -> str:
    """Show all news without labels"""
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@tp.no_type_check
@route("/add_label/")
def add_label() -> None:
    """Mark news"""
    s = get_session(engine)
    n_id = request.query["id"]
    n_label = request.query["label"]
    set_label(s, n_id, n_label)
    redirect("/news")


@tp.no_type_check
@route("/update")
def update_news() -> None:
    """Expand database"""
    s = get_session(engine)
    add_data(s, get_news(url="https://news.ycombinator.com/newest", n_pages=4))
    redirect("/news")


colors = {"good": "#bdedbb", "never": "#ffd3bb", "maybe": "#e9eae6"}


@tp.no_type_check
@route("/classify")
def classify_news() -> str:
    """Show classified news list"""
    s = get_session(engine)
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
