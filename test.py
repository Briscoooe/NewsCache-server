import json
import os
import asyncio

from newsapi import NewsApiClient
from newspaper import Article

newsapi = NewsApiClient(api_key=os.environ['NEWSAPI_KEY'])

'''
top_headlines = newsapi.get_top_headlines(q='trump',language='en')
url = top_headlines['articles'][1]['url']
article = Article(url)

article.download()
article.parse()

print (article.text)
'''
async def get_article_text(article_data):
    article = Article(article_data['url'])
    return await article.download()
    '''
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            filename = __.path.basename(url)
            with open(________, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(_____)
            return await response.release()
    '''
 
async def main():
    articles = newsapi.get_top_headlines(q='trump',language='en')
    print (len(articles['articles']))
    tasks = [get_article_text(article_data) for article_data in articles['articles']]
    await asyncio.gather(*tasks)
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())