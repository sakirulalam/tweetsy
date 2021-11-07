from tweetsy.tweet import Tweet, TweetLink
from datetime import datetime
from .utils import DATETIME_FORMAT

def parse_UserTweetsAndReplies(raw):    
    parsed_tweets_list = []
    entries = raw['data']['user']['result']\
    ['timeline']['timeline']['instructions'][0]['entries']
    
    for entry in entries:

        parsed_tweet = {}
        next_cursor = None

        # avoids TopicModules and cursor
        if entry['entryId'].split('-')[0] == 'tweet':
            tweet_id = entry['sortIndex']
            parsed_tweet['tweet_id'] = tweet_id
            
            result = entry['content']['itemContent']['tweet_results']['result']
            
            family = 'null' if result['__typename'] != 'Tweet' else None
            
            if family != 'null':
                legacy = result['legacy']
                if 'quoted_status_result' in result: family = 'quote'
                elif 'retweeted_status_result' in legacy: family = 'retweet'
                elif 'in_reply_to_status_id_str' in legacy: family = 'reply'
                elif 'card' in result: family = 'poll'
                else: family = 'vanilla'
                parsed_tweet['family'] = family

                # parse common legacy data
                parsed_tweet['user_id'] = result['core']['user']['rest_id']
                parsed_tweet['username'] = result['core']['user']['legacy']['screen_name']
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

                if family == 'retweet':
                    parsed_tweet['retweet'] = TweetLink(
                        legacy['retweeted_status_result']['result']['legacy']['conversation_id_str'],
                        legacy['retweeted_status_result']['result']['core']['user']['rest_id'],
                        legacy['retweeted_status_result']['result']['core']['user']['legacy']['screen_name']
                    )

                if family == 'quote':
                    parsed_tweet['quote'] = TweetLink(
                        legacy['quoted_status_id_str'],
                        result['quoted_status_result']['result']['core']['user']['rest_id'],
                        result['quoted_status_result']['result']['core']['user']['legacy']['screen_name'],
                    )
                
                if family == 'reply':
                    parsed_tweet['reply'] = TweetLink(
                        legacy['id_str'],
                        legacy['in_reply_to_user_id_str'],
                        legacy['in_reply_to_screen_name']
                    ) 

                parsed_tweet['family'] = family
                parsed_tweets_list.append(Tweet(pt=parsed_tweet))
        elif entry['entryId'].split('-')[0] == 'cursor':
            if entry['entryId'].split('-')[1] == 'bottom':
                next_cursor = entry['content']['value']
        
    return parsed_tweets_list, next_cursor

if __name__ == '__main__':
    pass
