import rbot
import sqlite3
import time
import datetime


SUBREDDIT = 'subreddit_here'
MATCH = ['search', 'terms', 'here']
OWNER = 'your_username_here'
QUERY = 'flair:selling'
WAIT = 60

sql = sqlite3.connect('hermes.db')
print('Connected to database')

cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS submissions(ID TEXT)')
sql.commit()
print('Table ready')

r = rbot.login()
print('Reddit login successful')


def collect_submissions():
    print('[' + str(datetime.datetime.now()) + ']: ' +
          'Collecting submissions...')

    try:
        submissions = list(r.search(QUERY, SUBREDDIT, 'new'))
    except Exception, e:
        print(type(e))
        return False

    submissions.reverse()

    for submission in submissions:
        if len(submission.title) > 99:
            sTitle = (submission.title[:96] + '...').lower()
        else:
            sTitle = submission.title.lower()

        s_id = submission.id
        sAuthor = submission.author.name

        if any(keyword in sTitle for keyword in MATCH):
            cur.execute('SELECT * FROM submissions WHERE ID=?', [s_id])
            if not cur.fetchone():
                cur.execute('INSERT INTO submissions VALUES(?)', [s_id])
                sql.commit()
                print('Added ' + s_id)
                private_message(s_id, sTitle, sAuthor)


def private_message(sub_id, sub_title, sub_author):
    url = 'https://reddit.com/r/' + SUBREDDIT + '/comments/' + sub_id
    message = '/u/' + sub_author +\
        ' is selling something on /r/' +\
        SUBREDDIT + ' that you might be interested in.\n\n' + url

    r.send_message(OWNER, sub_title, message)
    print('Message sent to /u/' + OWNER)


while True:
    collect_submissions()
    print('All submissions collected. Sleeping for ' +
          str(WAIT) + ' sec(s)...')

    time.sleep(WAIT)
