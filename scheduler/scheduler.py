import praw
import logging
import time
from datetime import datetime

print("Started!")
print("1")

logging.basicConfig(level = logging.INFO)

r = praw.Reddit("Klok-Poster")

print(r.user.me())

subreddit = r.subreddit("klokscheduler")

print("1")

x = datetime.today()

print("1")
print(str(datetime.now().hour))


def postpart(po, secs):
    try:
        time.sleep(secs)
        cryo = r.subreddit('thecryopodtohell')
        upd = r.submission(url = str(po.permalink))

        totext = upd.selftext
        totitle = upd.title

        cryo.submit(totitle, totext)

        print("1")

        po.delete()

    except Exception as e:
        with open('error.txt', 'w') as f:
            f.write(str(e))


print("1")

for submission in subreddit.new(limit = 1):
    print("1")

    author = submission.author
    title = str(submission.title)
    id_ = str(submission.id)

    fixit = []

    with open('parts.txt', 'r') as file:
        for line in file:
            linelen = len(line)
            newlinelen = linelen - 1
            if line[:newlinelen] not in fixit:
                fixit.append(line[:newlinelen])

    if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id_ not in fixit or \
       str(author).lower() == "thomas1672" and title[0:4].lower() == "test" and id_ not in fixit:

        print("FOUND")

        with open('parts.txt', 'a') as file:
            file.write(id_ + "\n")

        try:
            print("TRYING")

            tz = submission.comments[0]
            tz1 = tz.body
            tz2 = int(tz1) + 3

            print("TIME: " + str(tz2))

            totitle = title
            totext = submission.selftext
            now = datetime.now()

            if int(now.hour) > tz2:
                hours = int(24 + tz2) - int(now.hour)
                mins = hours * 60 - now.minute
                secs = int(mins) * 60
                tz.reply("Set for the time: " + str(tz1) + " on: " + str(x.day) + "/" + str(now.month))

            else:
                mleft = now.minute
                print("CURRENT TIME: " + str(now.hour))
                print("CURRENT - TODO = " + str(int(tz2 - int(now.hour))))
                mins = int(tz2 - int(now.hour)) * 60 - mleft
                secs = int(mins) * 60
                tz.reply("Set for the time: " + str(tz1) + " on: " + str(x.day) + "/" + str(now.month))

            print(str(secs))
            postpart(submission, secs)

        except Exception as e:
            print(str(e))
