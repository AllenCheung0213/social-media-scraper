import csv
import praw
from textblob import TextBlob
from datetime import datetime
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(
    client_id=config['REDDIT']['CLIENT_ID'],
    client_secret=config['REDDIT']['CLIENT_SECRET'],
    user_agent=config['REDDIT']['USER_AGENT']
)


hot_posts = reddit.subreddit('technews').hot(limit=500)

with open('reddit_posts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["target", "ids", "date", "flag", "user", "text"])

    for post in hot_posts:
        polarity = TextBlob(post.title).sentiment.polarity
        target = 0 if polarity < 0 else 2 if polarity == 0 else 4
        date = datetime.utcfromtimestamp(post.created_utc)
        formatted_date = date.strftime("%a %b %d %H:%M:%S %Z %Y")
        writer.writerow([target, post.id, formatted_date, "NO_QUERY", post.author, post.title])
