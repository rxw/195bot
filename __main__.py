#!./bin/python
# made by rxw
# wtfpl (2019)

from InstagramAPI import InstagramAPI
from PIL import Image
import requests
import random
import json
import praw
import time
import os

last_posted = None # keep track of new posts
hashtags = ['#meirl', '#me_irl', '#195', '#reddit', '#4chan', '#edgy', '#dank',
            '#memes', '#memebot', '#dankmemes', '#twitter', '#humor', '#humerous',
            '#meemee', '#lfl', '#f4f', '#mem']
            
formats = ['jpg', 'gif']
path = '/home/tato/src/195bot'
creds = json.loads(open('credentials.json', 'r').read())

# login to api's
InstaApi = InstagramAPI(creds['instagram']['username'], creds['instagram']['password'])
InstaApi.login()

reddit = praw.Reddit(client_id = creds['reddit']['client_id'], 
    client_secret = creds['reddit']['client_secret'],
    username = creds['reddit']['username'], 
    password = creds['reddit']['password'],
    user_agent = creds['reddit']['user_agent'])

if __name__ == '__main__':

    while True:
        post = reddit.subreddit('195').new().next()

        if post.id != last_posted and post.url[-3:] in formats:
            last_posted = post.id
            title, data = post.title, requests.get(post.url).content
            separator = '\n*'*10
            pounds = ' '.join(hashtags)
            
            ext = post.url[-3:]
            filename = '{}.{}'.format(post.id, ext)
            full_path = '{}/{}'.format(path, filename)
            cap = '{}\n/u/{}{}\n{}'.format(title, post.author.name, separator, pounds)

            with open(filename, 'wb') as f:
                f.write(data)

            image = Image.open(filename)
            image.save(filename)

            InstaApi.uploadPhoto(full_path, caption=cap)
            os.remove(full_path)

        time.sleep(60*random.randint(7,15))