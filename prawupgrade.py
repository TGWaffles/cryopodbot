import praw
from pw_bot import *
user_agent = ("CryoChecker 1.0")
r = praw.Reddit(user_agent = user_agent, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri="http://144.217.82.211:65010/authorize_callback")