import json
from datetime import datetime
from .utils import (
    get_client_id, post,
    DATETIME_FORMAT,
    GLOBAL_HEADERS,
    API_ENDPOINTS
)


class TweetLink():
    def __init__(self, tweet_id, user_id, username):
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.username = username
    
    def get_tweet(self):
        headers = GLOBAL_HEADERS
        TWEET_LINK_API = {
            'url': API_ENDPOINTS['tweet_detail'],
            'payload' : {
                'variables': json.dumps({
                    'focalTweetId' : self.tweet_id,
                    'with_rux_injections': False,
                    'includePromotedContent': True,
                    'withCommunity': True,
                    'withQuickPromoteEligibilityTweetFields': False,
                    'withTweetQuoteCount': True,
                    'withBirdwatchNotes': False,
                    'withSuperFollowsUserFields': True,
                    'withUserResults': True,
                    'withNftAvatar': False,
                    'withBirdwatchPivots': False,
                    'withReactionsMetadata': False,
                    'withReactionsPerspective': False,
                    'withSuperFollowsTweetFields': True,
                    'withVoice': True,
                }),
            }
        }
        headers['x-guest-token'] =  get_client_id()
        r = post(TWEET_LINK_API['url'], data=TWEET_LINK_API['payload'], headers=headers)
        raw = r.json()
        result = raw['data']['threaded_conversation_with_injections']\
            ['instructions'][0]['entries'][0]['content']['itemContent']\
                ['tweet_results']['result']
        legacy = result['legacy']
        parsed_tweet = {}
        parsed_tweet['tweet_id'] = self.tweet_id
        parsed_tweet['user_id'] = self.user_id
        parsed_tweet['username'] = self.username
        if 'quoted_status_result' in result: parsed_tweet['family'] = 'quote'
        else: parsed_tweet['family'] = 'vanilla'
        parsed_tweet['text'] = legacy['full_text']
        parsed_tweet['lang'] = legacy['lang']
        parsed_tweet['source'] = legacy['source']\
            .split('<')[-2].split('>')[-1]
        parsed_tweet['favorite_count'] = legacy['favorite_count']
        parsed_tweet['retweet_count'] = legacy['retweet_count']
        parsed_tweet['quote_count'] = legacy['quote_count']
        parsed_tweet['reply_count'] = legacy['reply_count']
        parsed_tweet['created_at'] = datetime.strptime(legacy['created_at'], DATETIME_FORMAT)
        parsed_tweet['media'] = []
        parsed_tweet['hashtags'] = [tag['text'] for tag in legacy['entities']['hashtags']]

        if parsed_tweet['family'] == 'quote':
            parsed_tweet['quote'] = TweetLink(
                legacy['quoted_status_id_str'],
                result['quoted_status_result']['result']['core']['user_results']['result']['rest_id'],
                result['quoted_status_result']['result']['core']['user_results']['result']['legacy']['screen_name'],
            )
                    
        # parse media
        if 'extended_entities' in legacy:
            for media in legacy['extended_entities']['media']:
                if media['type'] == 'photo':
                    parsed_tweet['media'].append({
                        'type': 'photo',
                        'source': media['media_url_https'],
                        'url': media['expanded_url'],
                    })
                if media['type'] == 'video':
                    parsed_tweet['media'].append({
                        'type': 'video',
                        'view_count': media['mediaStats']['viewCount'],
                        'source': media['video_info']['variants'],
                        'url': media['expanded_url'],
                    })
                if media['type'] == 'animated_gif':
                    parsed_tweet['media'].append({
                        'type': 'gif',
                        'source': media['video_info']['variants'],
                        'url': media['expanded_url'],
                    })
                                        
        
        return Tweet(pt=parsed_tweet)

    @property
    def absolute_url(self):
        return f'https://twitter.com/{self.username}/status/{self.tweet_id}'
    
    @property
    def user_absolute_url(self):
        return f'https://twitter.com/{self.user_id}'

class Tweet():
    """Tweet object. Contains the following data:
    tweet_id (a unique identifier for any tweet)
    user_id (the author's account id)
    username (thet author's current* account username)
    family [vanilla | retweet | reply | quote | poll | null]
    text [eng, bn, und etc.]
    source [web, android, mobile etc]
    favorite_count
    retweet_count
    reply_count
    quote_count
    created_at (datetime object)
    media <dict>
    hashtags
    retweet <Object: TweetLink>
    quote <Object: TweetLink>
    reply <Object: TweetLink>
    poll <Object: Poll>
    """
    def __init__(self, pt):
        self.tweet_id = pt['tweet_id']
        self.user_id = pt.get('user_id', None)
        self.username = pt.get('username', None)
        self.family = pt.get('family', None)
        self.text = pt.get('text', None)
        self.lang = pt.get('lang', None)
        self.source = pt.get('source', None)
        self.favorite_count = pt.get('favorite_count', None)
        self.retweet_count = pt.get('retweet_count', None)
        self.reply_count = pt.get('reply_count', None)
        self.quote_count = pt.get('quote_count', None)
        self.created_at = pt.get('created_at', None)
        self.media = pt.get('media', None)
        self.hashtags = pt.get('hashtags', None)
        self.retweet = pt.get('retweet', None)
        self.quote = pt.get('quote', None)
        self.poll = pt.get('poll', None)
        self.reply = pt.get('reply', None)
    
    @property
    def absolute_url(self):
        return f'https://twitter.com/{self.username}/status/{self.tweet_id}'
    
    def serialize(self):
        return vars(self)
