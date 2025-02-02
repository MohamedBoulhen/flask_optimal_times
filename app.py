import praw
import time
from datetime import datetime
from collections import defaultdict, Counter

# Reddit API credentials
CLIENT_ID = 'YvlRuFWXP60-5GnKiCQ37w'
CLIENT_SECRET = '6X9A9_CrfXgHMc0PXft04OU1NfrOhw'
USER_AGENT = 'timetopost.io/1.0 by Time-Hat1565'

# Set up Reddit API client
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def fetch_subreddit_data(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    active_users = subreddit.active_user_count
    top_posts = subreddit.top(time_filter='week', limit=100)  # Adjust limit for more data

    post_times_by_day = defaultdict(list)
    
    for post in top_posts:
        post_time = datetime.utcfromtimestamp(post.created_utc)
        post_times_by_day[post_time.weekday()].append(post_time.hour)

    best_times_by_day = {}
    
    for day, hours in post_times_by_day.items():
        if hours:
            best_hour = Counter(hours).most_common(1)[0][0]
            best_times_by_day[day] = best_hour
    
    return active_users, best_times_by_day

def print_best_times(active_users, best_times_by_day):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print(f"Active users: {active_users}")
    for day_index, best_hour in best_times_by_day.items():
        print(f"Best time to post on {days[day_index]}: {best_hour}:00 UTC")

# Test function
active_users, best_times = fetch_subreddit_data('SaaS')
print_best_times(active_users, best_times)

