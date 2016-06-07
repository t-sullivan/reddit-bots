from lxml import html
from time import sleep
import requests
import sqlite3
import re
import rbot


URL = 'http://www.scandal-heaven.com'
SUBREDDIT = 'scandalband'
WAIT = 600

# Store submitted posts in DB to avoid reposts
sql = sqlite3.connect('scandal.db')
print('Connected to database')

cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(ID TEXT)')
sql.commit()
print('Table ready')

r = rbot.login()


def collect_posts():
    page = requests.get(URL + '/tags/front-page')
    tree = html.fromstring(page.text)
    posts = tree.xpath('//div[@class="posthead"]//a')
    posts.reverse()
    prog = re.compile('#(\d*)')
    print(len(posts))

    for post in posts:
        post_title = post.text
        post_link = URL + post.attrib['href']
        post_id = re.search(prog, post.attrib['href']).group(1)

        cur.execute('SELECT * FROM posts WHERE ID=?', [post_id])
        if not cur.fetchone():
            cur.execute('INSERT INTO posts VALUES(?)', [post_id])
            sql.commit()
            print('Added post #' + post_id)
            submit_post(post_title, post_link)


def submit_post(title, link):
    r.submit(SUBREDDIT, title, url=link)
    print('Post submitted to /r/' + SUBREDDIT +
          '\nSleeping for ' + str(WAIT) + ' sec(s)...')
    sleep(WAIT)  # Wait 10 minutes between posts


while True:
    collect_posts()
    print('All posts submitted, checking again in 30 minutes...')
    sleep(1800)  # Wait 30 mins between scraping the site
