import praw

r = praw.Reddit("Klok-Poster")

cryo = r.subreddit('thecryopodtohell')
upd = r.submission(url=str("https://www.reddit.com/r/klokscheduler/comments/5npysl/part_301/"))

totext = upd.selftext
totitle = upd.title

cryo.submit(totitle, totext)
