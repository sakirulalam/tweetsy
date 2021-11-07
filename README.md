# Tweetsy
Tweetsy uses Twitter's underlying API to fetch user information and tweets and present it in a human-friendly way. What makes Tweetsy special is that everything is an object here. So it makes it very easier for the end users to store the data however they want, i.e. CSV, HTML or even in cloud database. This will become more clear in the following sections.
## Getting user data
This package was originally designed to get user information (i.e. name, number of follower, profile image url) and tweets, given the username of the user. It all starts with the `User` class of the `user` module of this package.
```python
>>> # get data from https://twitter.com/DrTedros
>>> from tweetsy.user import User
>>> user = User('DrTedros')
>>> user
<tweetsy.user.User object at 0x0000007B0C5C74F0>
>>> user.name
'Tedros Adhanom Ghebreyesus'
```
As it can be seen, the when we create an instance of the `User` object providing the username of a user, we can access relevant data of the user. The full API is given at the end of this page. Here is how we get the profile picture, number of followers of the user and the date when the profile was created.
```python
>>> user.profile_image
{'normal': 'https://pbs.twimg.com/profile_images/1337835478704291842/O1A5QF3x_normal.png', 'medium': 'https://pbs.twimg.com/profile_images/1337835478704291842/O1A5QF3x_200x200.png', 'large': 'https://pbs.twimg.com/profile_images/1337835478704291842/O1A5QF3x_400x400.png'}
>>> user.profile_image['large']
'https://pbs.twimg.com/profile_images/1337835478704291842/O1A5QF3x_400x400.png'
>>> user.follower_count
1573518
>>> user.created_at
datetime.datetime(2010, 9, 12, 13, 9, 27, tzinfo=datetime.timezone.utc)
```
The `created_at` attribute returns a python `datetime` object instead of plain text, which makes it a lot easier to manipulate and use the data for in future.
## Getting user tweets
The `get_tweets` method of the `User` class fetches the tweets. This method returns a tuple of two elements, the first one is a list of `Tweet` objects and the later one is `cursor`, which works as a marker and is used to get the next tweets.
```python
>>> tweets, cursor = user.get_tweets(5)
>>> tweets[0]
<tweetsy.tweet.Tweet object at 0x0000007B0EFFF430>
>>> tweets[0].absolute_url
'https://twitter.com/DrTedros/status/1457104908633640966'
>>> cursor
'HBaAwLmhjM3FuCgAAA=='
>>> next_tweets, next_cursor = user.get_tweets(5, cursor=cursor)
```
### The `Tweet` Object
The tweet object comes with a lot of attributes.
```python
>>> tweet = tweets[0]
>>> tweet.text
'RT @benphillips76: This photo of Tuvalu's virtual address to the Climate Confer ence says everything that should need to be said.  #COP26 ht.'
>>> tweet.tweet_id
'1457104908633640966'
>>> tweet.source
'Twitter for iPhone'
>>> tweet.family
'retweet'
```
The `family` attribute is very crucial. Not all tweets are plain texts or images, some are retweets of another tweet, some are quoted tweets. In this package the retweets and quotes contain their own attributes, which are `TweetLink` object, which refers to the original parent tweet. A `TweetLink` instane contains 3 attributes, `tweet_id`, `user_id`, `username`. This is better shown with an example.
```python
>>> tweet.family
'retweet'
>>> tweet.retweet
<tweetsy.tweet.TweetLink object at 0x0000007B0C60FAF0>
>>> tweet.retweet.absolute_url
'https://twitter.com/benphillips76/status/1456629120973017089'
```
This gives us the tweet by benphillips76, which was retweeted by DrTedros.

The `TweetLink` contains a method called `get_tweet`, which can be used to fetch the parent tweet data, i.e. another `Tweet` instance.
```python
>>> new_tweet = tweet.retweet.get_tweet()
>>> new_tweet
<tweetsy.tweet.Tweet object at 0x0000007B0C5C7550>
>>> new_tweet.retweet_count
8909
>>> new_tweet.media
[{'type': 'photo', 'source': 'https://pbs.twimg.com/media/FDb8W1UXEAAgxiA.jpg', 'url': 'https://twitter.com/benphillips76/status/1456629120973017089/photo/1'}]
```
So from now on, the `new_tweet` can be treated like any other `Tweet` object.

## Installation
The package hasn't been published in PyPI yet. Since the package is very minimal, one can just simply do this:
```
C:\Users\USER> git clone https://github.com/binarysakir/tweetsy
C:\Users\USER> cd tweetsy
C:\Users\USER> pip install requirements.txt
C:\Users\USER> python
>>> from tweetsy.user import User
```

## Full description of classes
### `User`
To initialize, provide the username of the Twitter account.
Attributes:
* `user_id`: User id. The username can change over time but the user id does not.
* `name`: Mame of the user profile
* `tweet_count`: Total number of tweets of a user.
* `created_at`: Time of the account creation. Python `datetime` object.
* `follower_count`: How many accounts are following the user.
* `following_count`: How many accounts the user is following.
* `description`: Bio of the account.
* `profile_image`: Profile image of the user. It's a `dict` containing the URL of the profile image of 3 different sizes- `normal`, `medium` and `large`.
* `profile_banner`: URL of the account banner or the cover picture.
* `media_count`: Number of media uploaded by the user.
* `verified`: Boolean data type.
Methods:
* `get_tweets(count, reply, cursor)`: `count` indicates the number tweets to be fetched, default is `20`. `reply` accepts boolean value, default is `False`. If set to `True` then it will fetch "Tweets and Replies" section of the profile. `cursor` is by default `None`, so it fetches the first `count` tweets of the profile if not set to anything else. This method returns a tuple of a list of tweets (`Tweet` objects) and cursor. See usage in above examples. **IMPORTANT** The `get_tweets` may or may not return the same number of tweets as `count`. Generally the number of returned tweets is one more or less than the given argument.
* `serialize()`: Returns a dictionary of all the available attributes. It is just an alternative of Python's built-in `vars` method.

### `TweetLink`
It works as a reference to a tweet without actually fetching the tweet. To initialize, provide the following: `tweet_id`, `user_id`, `username`.
Attributes:
* `tweet_id`
* `user_id`
* `username`
* `absolute_url`
* `user_absolute_url`
Methods:
* `get_tweet()`: Returns a `Tweet` object of the tweet.
This class can be used to fetch a tweet without using the a `User` object.

### `Tweet`
This tweet should not be be initialized manually since it takes modified JSON data generated by `parse_UserTweetsAndReplies` function of `parser.py`.
Attributes:
* `tweet_id`
* `user_id`
* `username`
* `family`: It has 6 possible values: `vanilla`, `retweet`, `reply`, `quote`, `poll`, `null`. Vanilla is just a plain original tweet. Retweet, reply and quote indicates their own meaning respectively. The poll family indicates the tweet is a poll. Null indicated the tweet is empty.
* `text`: Text of the tweet. Might be truncated in case it's a retweet.
* `lang`: Language of the tweet.
* `source`: From which device the tweet was posted.
* `favorite_count`
* `retweet_count`
* `reply_count`
* `quote_count`
* `created_at`
* `media`: A `dict` containing the media URLs of the tweet.
* `hashtags`
* `retweet`: If the tweet is a retweet, this will be a `TweetLink` object, otherwise `None`.
* `quote`: If the tweet is a quote, this will be a `TweetLink` object, otherwise `None`.
* `poll`: If the tweet is a poll, this will be a `TweetLink` object, otherwise `None`.
* `reply`If the tweet is a poll, this will be a `TweetLink` object, otherwise `None`.

It is adviced to fetch the `favorite_count`, `retweet_count`, `reply_count` and the `quote_count` of a vanilla tweet and not of a quote or retweet tweet.

## Bugs
Be sure to report bugs!

## TODO
- Fetch Twitter poll tweet data
- Fix number of returned tweets problems
- Get user info from user id

## Disclaimer
I wrote this package only for using the knowledge of OOP and API. This package is under MIT license. I am not responsible for any kind of abuse of this package.
