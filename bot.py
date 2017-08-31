#!/usr/bin/python
import logging
import random
import time

import praw

# Imports all passwords from a hidden file ;)
from pw_bot import *
from reddit.strings import *

logging.basicConfig(level = logging.INFO)

# if str(submission.title)[0:4] for submission in subreddit.get_new(limit = 1):
# 	author = submission.author
# 	print(author)
# 	time.sleep(5)
# 	if str(author).lower() == "klokinator":
# 		print("TEST!")
# 		time.sleep(5).lower() == "part":


def remove(filename, who):
    with open(filename, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if str(who) != i:
                f.write(i)
        f.truncate()


def getlist(filename, otherls = None):
    templs = []

    if otherls is None:
        otherls = templs

    with open(filename, 'r') as file:
        for line in file:
            linelen = len(line)
            newlinelen = linelen - 1
            if line[:newlinelen] not in otherls:
                templs.append(line[:newlinelen])

    return templs


def write(file, stuff):
    with open(file, 'a') as file:
        file.write(str(stuff))


def domsgs():
    messages = r.inbox.messages()

    # For every message in the messages you just fetched:
    for message in messages:
        print("Opening message!")

        alreadyin = getlist('list.txt')
        already_done = getlist('done.txt')

        # If the message talks about subscription, and if the author hasn't already been added and the id isn't done:
        if "unsubscribe" in str(message.body).lower() and str(message.author) in alreadyin and str(
                message.id) not in already_done:
            message.reply(pm_unsub)

            remove('list.txt', message.author)
            already_done.append(message.id)
            write('done.txt', str(message.id) + "\n")

        elif "subscribe" in str(message.body).lower() and str(message.author) not in alreadyin \
                and str(message.id) not in already_done:
            print("Adding someone! - " + str(message.author))

            # Double check to attempt to double-post proof.
            if str(message.author) not in alreadyin:

                # Write the sender's name in the username list.
                # Tells the sender they've been added.
                try:
                    write('list.txt', str(message.author) + "\n")
                    message.reply(pm_sub)
                except Exception as e:
                    print(e)
                time.sleep(2)

                # Adds their name to the ID list and stuff.
                alreadyin.append(message.author)
                already_done.append(message.id)
                write('done.txt', str(message.id) + "\n")


def dothrd():
    # For thread in the subreddit, out of the newest thread.
    for submission in subreddit.get_new(limit = 1):
        time.sleep(3)

        # Set variables to prevent annoying the reddit api.
        author = submission.author
        title = str(submission.title)
        id_ = str(submission.id)

        # Same as message checking but for threads.
        fixit = getlist('parts.txt')

        # If the author is Klok and it begins with part, do this:
        if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id_ not in fixit or str(
                author).lower() == "thomas1672" and title[0:4].lower() == "test" and id_ not in fixit:

            write('parts.txt', id_ + "\n")

            with open('lastpart.txt', 'r') as file:
                lastprt = file.readline()

            nxtparts = r.submission(lastprt)
            nxtpart = nxtparts.comments[0]

            add = nxtpart.body + "\n" + "\n" + "**[" + submission.title + "](" + submission.permalink + ")**"
            nxtpart.edit(add)

            prevurl = r.submission(id = nxtpart.parent_id).permalink
            uwc = []
            wc = 0

            for i in str(submission.selftext).split():
                if i not in uwc:
                    wc += 1
                    uwc.append(i)

            # Post the comment on the thread.
            postedcomment = submission.add_comment(replystr.format(chars = str(len(submission.selftext)),
                                                                   words = str(len(str(submission.selftext).split())),
                                                                   uwords = str(wc),
                                                                   prevurl = prevurl))

            with open('lastpart.txt', 'w') as file:
                file.write(str(postedcomment.permalink))

            submission.set_flair("STORY", "story")

            # Sticky the comment that was just posted.
            postedcomment.mod.distinguish(sticky = True)

            # Get the index list's ID.
            toedit = r.submission(id = '56tvbw')
            time.sleep(2)

            # Add post that was just posted to the index list.
            tempedit = toedit.selftext
            putin = tempedit + "\n" + "\n" + "[" + submission.title + "](" + submission.permalink + ")"

            time.sleep(2)
            toedit.edit(putin)
            time.sleep(2)

            if title[0:4].lower() != "test":

                # Put all users in the username file into a list, then:
                alreadyin = getlist('list.txt')
                finished = []

                # For every name in the list, send them this message with the link to the part.
                for name in alreadyin:
                    try:
                        r.redditor(name).message("New Post!", pmbody.format(title = title,
                                                                            permalink = submission.permalink))

                        finished.append(str(name))
                    except Exception as ex:
                        print(ex)
                        print(name)
                        write('offenders.txt', name + "\n")

                    time.sleep(1)

                time.sleep(10)

                todo = getlist('list.txt', finished)

                for name in todo:
                    try:
                        r.redditor(name).message("New Post!", pmbody.format(title = title,
                                                                            permalink = submission.permalink))
                    except Exception as ex:
                        print(ex)
                        print(name)

                        write('offenders.txt', name + "\n")
                        torem = name + "\n"
                        remove('list.txt', torem)

                    time.sleep(1)


def docomts():
    # Loops through every comment in the sub.
    for comment in subreddit.comments():

        # Opens file with comment ids.
        already_done = getlist('done.txt')

        # If someone's tagging us and we've not processed their comment:
        if not ("/u/cryopodbot" in str(comment.body).lower() and str(comment.id) not in already_done):
            continue

        # If it's talking about the post, comment the post.
        if "post" in str(comment.body).lower():

            # Make sure the bot doesn't respond to itself.
            if str(comment.author).lower() != "cryopodbot":

                # Reply!
                comment.reply(replystr2)

                # Post the ID to a file to prevent duplicates.
                write('done.txt', str(comment.id) + "\n")

        # If the post wants a flair and it's me or Klok:
        elif "flair info" in str(comment.body).lower() and (str(comment.author).lower() == "thomas1672" or
                                                            str(comment.author).lower() == "klokinator"):

                flairsubmtoset = r.submission(id = str(comment.parent_id)[-6:])

                # Flair and stop duplicate flairing (would only waste processor time)
                flairsubmtoset.mod.flair("INFO", "info")
                write('done.txt', str(comment.id) + "\n")

        elif "flair question" in str(comment.body).lower() and (str(comment.author).lower() == "thomas1672" or
                                                                str(comment.author).lower() == "klokinator"):

                flairsubmtoset = r.submission(id = str(comment.parent_id)[-6:])

                flairsubmtoset.mod.flair("QUESTION", "question")
                write('done.txt', str(comment.id) + "\n")

        elif str(comment.author).lower() != "cryopodbot":
            select = int(random.randint(0, 10))

            try:
                reply = randreply[select]
            except IndexError:
                reply = randdef

            comment.reply(reply)

            write('done.txt', str(comment.id) + "\n")


if __name__ == '__main__':
    user_agent = "CryoBot 1.0"

    # Starts the main section of the reddit bot and assigns it to r.
    r = praw.Reddit(
        user_agent = user_agent,
        username = REDDIT_USERNAME,
        password = REDDIT_PASS,
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET
    )

    # Connects to the TCTH sub.
    subreddit = r.subreddit("thecryopodtohell")

    domsgs()
    dothrd()
    docomts()