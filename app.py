from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

CLIENT_ID = 'YvlRuFWXP60-5GnKiCQ37w'
CLIENT_SECRET = '6X9A9_CrfXgHMc0PXft04OU1NfrOhw'
USER_AGENT = 'timetopost.io/1.0 by Time-Hat1565'

def fetch_subreddit_data(subreddit):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': 'Time-Hat1565',  # Replace with your Reddit username
        'password': 'lala-cmoi'   # Replace with your Reddit password
    }
    headers = {'User-Agent': USER_AGENT}

    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = response.json()['access_token']
    headers['Authorization'] = f'bearer {token}'

    about_url = f'https://oauth.reddit.com/r/{subreddit}/about'
    about_response = requests.get(about_url, headers=headers)
    active_users = about_response.json()['data']['active_user_count']

    posts_url = f'https://oauth.reddit.com/r/{subreddit}/new'
    posts_response = requests.get(posts_url, headers=headers)
    posts = posts_response.json()['data']['children']

    activity_data = {}
    current_time = datetime.datetime.utcnow()
    twenty_four_hours_ago = current_time - datetime.timedelta(hours=24)

    for post in posts:
        created_time = datetime.datetime.fromtimestamp(post['data']['created_utc'])
        if created_time < twenty_four_hours_ago:
            continue

        hour = created_time.strftime('%H:%M')
        if hour in activity_data:
            activity_data[hour] += 1
        else:
            activity_data[hour] = 1

    best_time = max(activity_data, key=activity_data.get) if activity_data else 'N/A'

    return {
        'active_users_online': active_users,
        'best_time_to_post_today': best_time,
        'activity_data': activity_data
    }

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    subreddit = request.args.get('subreddit')
    data = fetch_subreddit_data(subreddit)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
