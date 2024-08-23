import praw
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

# reddit api
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# given subreddit name, scrapes posts with a specific limit
def scrape_subreddit(subreddit_name, limit=None):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.new(limit=limit):
        post_data = {
            'id': post.id,
            'title': post.title,
            'author': post.author.name if post.author else '[deleted]',
            'created_utc': post.created_utc,
            'score': post.score,
            'body': post.selftext,
            'url': post.url,
            'num_comments': post.num_comments
        }
        
        # Fetch comments
        post.comments.replace_more(limit=0)  # Flatten comment tree
        comments = []
        for comment in post.comments.list():
            comment_data = {
                'id': comment.id,
                'author': comment.author.name if comment.author else '[deleted]',
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc
            }
            comments.append(comment_data)
        
        post_data['comments'] = comments
        
        posts.append(post_data)
        print(f"Scraped post: {post.id}")
        
        # reddit rates
        time.sleep(2)
    
    return posts


japan_travels_posts = scrape_subreddit('JapanTravel', limit=100)

# save to json
with open('japanTravel_posts.json', 'w', encoding='utf-8') as f:
    json.dump(japan_travels_posts, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(japan_travels_posts)} posts! :D")