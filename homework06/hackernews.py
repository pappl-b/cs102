from bottle import route, run, template, request, redirect 

from scraputils import get_news
from db import News, session, add_data, set_label
from bayes import NaiveBayesClassifier


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    n_id = request.query["id"]
    n_label = request.query["label"]
    set_label(session(), n_id, n_label)
    redirect("/news")


@route("/update")
def update_news():
    add_data(session(), get_news(url="https://news.ycombinator.com/", n_pages=12))
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
