from newspaper import Article, news_pool
from flask import jsonify


def trim_articles(articles):
    trimmed_articles = []
    for article in articles:
        trimmed_article = {
            'title': article.title,
            'article_html': article.article_html,
            'publish_date': article.publish_date,
            'authors': article.authors,
            'summary': article.summary,
            'imgs': list(article.imgs),
            'text': article.text,
            'url': article.url
        }
        trimmed_articles.append(trimmed_article)
    return trimmed_articles


def download_articles_from_urls(urls):
    articles = []
    for url in urls:
        articles.append(Article(url))

    news_pool.set_articles(articles)
    news_pool.join()

    trimmed_articles = trim_articles(articles)
    return trimmed_articles
