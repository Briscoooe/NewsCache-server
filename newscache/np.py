from newspaper import Article, news_pool


def download_articles_from_urls(urls):
    articles = []
    for url in urls:
        articles.append(Article(url))

    news_pool.set_articles(articles)
    news_pool.join()

    return articles
