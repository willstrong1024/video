#!/usr/bin/python3

import json, os, praw, sys

if len(sys.argv) != 2:
    exit()

with open("config/reddit.json", "r") as f:
    config = json.load(f)

reddit = praw.Reddit(client_id=config['id'],
        client_secret=config['secret'],
        user_agent=config['user_agent'])
subreddit = sys.argv[1]

path = "/tmp/video/posts/"
os.mkdir(path)

with open(path + "name", "w") as f:
    f.write(subreddit)

for i, post in enumerate(reddit.subreddit(subreddit).top(time_filter="day", limit=5)):
    directory = path + "post" + str(i)
    os.mkdir(directory)

    with open(directory + "/body", "w") as f:
        f.write(post.selftext)

    with open(directory + "/head", "w") as f:
        f.write(post.title)

    with open(directory + "/id", "w") as f:
        f.write(post.id)

    with open(directory + "/url", "w") as f:
        f.write("https://www.reddit.com" + post.permalink)
