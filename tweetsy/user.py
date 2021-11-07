import  json
from datetime import datetime
from .parser import parse_UserTweetsAndReplies
from .utils import (
    get_client_id, post, change_profile_url,
    DATETIME_FORMAT,
    GLOBAL_HEADERS,
    API_ENDPOINTS
)

class User():

    headers = GLOBAL_HEADERS

    def __init__(self, username):
        """ Returns user profile data
        """

        self.username = username
        
        USER_INFO_API = {
            'url': API_ENDPOINTS['user_init_api'],
            'payload' : {
                'variables': json.dumps({
                    'screen_name' : self.username,
                    'withHighlightedLabel': True,
                }),
            }
        }
        
        self.headers['x-guest-token'] =  get_client_id()
        r = post(USER_INFO_API['url'], data=USER_INFO_API['payload'], headers=self.headers)
        user_info_json = r.json()
        
        legacy = user_info_json['data']['user']['legacy']

        self.user_id = user_info_json['data']['user']['rest_id']
        self.name = legacy['name']
        self.tweet_count = legacy['statuses_count']
        self.created_at = datetime.strptime(legacy['created_at'], DATETIME_FORMAT)
        self.follower_count = legacy['followers_count']
        self.following_count = legacy['friends_count']
        self.description = legacy['description']
        profile_image_normal = legacy['profile_image_url_https']
        self.profile_image = {
            'normal': profile_image_normal,
            'medium': change_profile_url(profile_image_normal, 200),
            'large': change_profile_url(profile_image_normal, 400),
        }
        self.profile_banner = legacy['profile_banner_url']
        self.media_count = legacy['media_count']
        self.verified = legacy['verified']

    def get_tweets(self, count=20, reply=False, cursor=None):

        """Returns a list of tweets and cursor. Count should be <= 500.
        The amount of tweets that twitter will return may become count ± 1,
        it is variable.
        """

        USER_TWEETS_API = {
            'url': API_ENDPOINTS['user_tweets_replies'] if reply else API_ENDPOINTS['user_tweets'],
            'payload': {
                'variables': json.dumps({
                    'userId': f'{self.user_id}',
                    'count': count+1,
                    'withHighlightedLabel': True,
                    'withTweetQuoteCount': True,
                    'includePromotedContent': False,
                    'withQuickPromoteEligibilityTweetFields': False,
                    'withTweetResult': True,
                    'withReactions': False,
                    'withSuperFollowsTweetFields': False,
                    'withSuperFollowsUserFields': False,
                    'withUserResults': False,
                    'withVoice': False,
                    'withNonLegacyCard': True,
                    'withBirdwatchPivots': False,
                    'withReactionsMetadata': False,
                    'withReactionsPerspective': False,
                    'cursor': f'{cursor}' if cursor else None
                }),
            }
        }
        self.headers['x-guest-token'] =  get_client_id()
        r = post(USER_TWEETS_API['url'], data=USER_TWEETS_API['payload'], headers=self.headers)
        return parse_UserTweetsAndReplies(r.json())
    
    def serialize(self):
        return vars(self)


if __name__ == '__main__':
    pass

