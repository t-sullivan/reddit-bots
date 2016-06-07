import praw

# see https://www.reddit.com/dev/api
app_id = ''
app_secret = ''
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_ua = ''
app_refresh = ''

r = praw.Reddit(app_ua)


def login():
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    refresh()
    return r


def refresh():
    r.refresh_access_information(app_refresh)
