import csv
import praw
from textblob import TextBlob
from datetime import datetime
import time
import configparser

# Load configuration settings from config file
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=config['REDDIT']['CLIENT_ID'],
    client_secret=config['REDDIT']['CLIENT_SECRET'],
    user_agent=config['REDDIT']['USER_AGENT']
)

# Function to fetch posts and write data to CSV
def fetch_and_write_posts(subreddit_name, limit, filename):
    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=limit)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["target", "ids", "date", "flag", "user", "text"])

        for post in hot_posts:
            polarity = TextBlob(post.title).sentiment.polarity
            target = 0 if polarity < 0 else 2 if polarity == 0 else 4
            date = datetime.utcfromtimestamp(post.created_utc)
            formatted_date = date.strftime("%a %b %d %H:%M:%S %Z %Y")
            writer.writerow([target, post.id, formatted_date, "NO_QUERY", str(post.author), post.title])
            time.sleep(0.05)  # Sleep to avoid hitting rate limits

# Fetch and write posts data to CSV
fetch_and_write_posts('funny', 10000, 'reddit_posts.csv')

