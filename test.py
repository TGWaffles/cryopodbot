#!/usr/bin/python
import praw
import time
user_agent = ("CryoBot 1.0")

r = praw.Reddit(user_agent = user_agent)

subreddit = r.get_subreddit("test")
r.login("CryopodBot", "KlokIsBae12")
submission = r.get_submission(submission_id='56t82u')
time.sleep(2)
toedit = submission.selftext
putin = toedit + "\n" + "\n" + "test3!"
time.sleep(3)
submission.edit(putin)
