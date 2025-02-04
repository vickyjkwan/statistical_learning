import requests
import bs4
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import datetime as dt
from pymongo import MongoClient
# Define the MongoDB database and table
db_cilent = MongoClient()
db = db_cilent['nyt']
table = db['meta']

# Query the NYT API once
def single_query(link, payload):
    response = request.get(link, params=payload)
    if response.status_code != 200:
        print 'WARNING', response.status_code
    else:
        return response.json()

# Determine if the results are more than 100 pages
def more_than_100_pages(total_page):
    if total_page > 100:
        pages_left = min(total_page - 100, 100)
        return 100, pages_left, True
    else:
        return pages_left, 0, False

# Looping through the pages give the number of pages
def loop_through_pages(total_pages, link, payload, table):
    for i in range(total_pages):
        if i % 50 == 0:
            print ' || Page ', i
        payload['page'] = str(i)
        content = single_query(link, payload)
        meta_lst = content['response']['docs']

        for meta in meta_lst:
            try:
                table.insert(meta)
            except DuplicateKeyError:
                print 'DUPS!'

# Scrape the meta data (link to article and put it into Mongo)
def scrape_meta(days=1):

    # The basic parameters for the NYT API
    link = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    payload = {'api-key': '74c73309c1052e6aa1785df7cd5cef8c:9:69947183'}

    today = dt.datetime(2015, 1, 28)
    for day in range(days):
        payload['end_date'] = str(today).replace('-','')
        half_day = today - dt.timedelta(hours=12)
        payload['begin_date'] = str(yesterday).replace('-','')
        print 'Scraping period: %s - %s ' % (str(yesterday), str(today))

        today -= dt.timedelta(days=2)

        content = single_query(link, payload)
        hits = content['response']['meta']['hits']
        total_pages = (hits / 10) + 1
        print 'HITS', hits

        newest_sort_pages, oldest_sort_pages, grt_100 = more_than_100_pages(total_pages)

        if grt_100:
            new_payload = payload.copy()
            old_payload = payload.copy()
            new_payload['sort']= 'newest'
            old_payload['sort'] = 'oldest'

        loop_through_pages(newest_sort_pages, link, new_payload, table)
        loop_through_pages(oldest_sort_pages, link, old_payload, table)


# Get all the links, visit the page and scrape the content
def get_articles(table):
    links = table.find({},{'web_url': 1})

    counter = 0
    for uid_link in links:
        counter += 1
        if counter % 100 == 0:
            print 'Count: ', counter, ' '
            print uid
        uid = uid_link['_id']
        link = uid_link['web_url']
        html = requests.get(link).content
        soup = bs4.BeautifulSoup(html, 'html.parser')

        article_content = '\n'.join([i.text for i in soup.select('p.story-body-text')])
        if not article_content:
            article_content = '\n'.join([i.text for i in soup.select('.caption-text')])
        if not article_content:
            article_content = '\n'.join([i.text for i in soup.select('[itemprop="description"]')])
        if not article_content:
            article_content = '\n'.join([i.text for i in soup.select('#nytDesignBody')])
        else:
            article_content = ''

        table.update({'_id': uid}, {'$set': {'raw_html': html}})
        table.update({'_id': uid}, {'$set': {'content_txt': article_content}})

if __name__ == '__main__':
    scrape_meta()
    get_articles(table)                
