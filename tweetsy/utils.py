import requests

post = requests.post

GUEST_TOKEN_API = 'https://api.twitter.com/1.1/guest/activate.json'
DATETIME_FORMAT = '%a %b %d %X %z %Y'

API_ENDPOINTS = {
    'user_init_api': 'https://twitter.com/i/api/graphql/4ti9aL9m_1Rb-QVTuO5QYw/UserByScreenNameWithoutResults',
    'user_tweets_replies': 'https://twitter.com/i/api/graphql/TcBvfe73eyQZSx3GW32RHQ/UserTweetsAndReplies',
    'user_tweets': 'https://twitter.com/i/api/graphql/9R7ABsb6gQzKjl5lctcnxA/UserTweets',
    'tweet_detail': 'https://twitter.com/i/api/graphql/xzEfo9VRrMWI8a-5H2hMqw/TweetDetail'
}

GLOBAL_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'origin': 'https://twitter.com',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
}


def change_profile_url(url, d):
    return '_'.join(url.split('_')[:-1]) + '_' + url.split('_')[-1].replace('normal', f'{d}x{d}')

def get_client_id():
    r = post(GUEST_TOKEN_API, headers=GLOBAL_HEADERS)
    return str((r.json())['guest_token'])


