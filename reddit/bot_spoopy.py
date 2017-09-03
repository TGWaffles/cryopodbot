#!/usr/bin/python
import sys
import logging
import praw
import os
import re
import OAuth2Util
import random
import time
from praw.models import Submission

# Imports all passwords from a hidden file ;)
logging.basicConfig(level=logging.INFO)
user_agent = "CryoBot 2.0"

# Starts the main section of the reddit bot and assigns it to r.
r = praw.Reddit(user_agent=user_agent)

# Connects to the TCTH sub.
subreddit = r.subreddit("thecryopodtohell")

# Logs into Bot's Account from hidden file above.
oauth = OAuth2Util.OAuth2Util(r)
oauth.refresh(force=True)


#  for submission in subreddit.get_new(limit = 1):
# 	author = submission.author
# 	print(author)
# 	time.sleep(5)
# 	if str(author).lower() == "klokinator":
# 		print("TEST!")
# 		time.sleep(5)
# if str(submission.title)[0:4].lower() == "part":

# Fetches all messages sent to the bot.
def removel(who):
    listfile = open("../user_list.txt", "r+")
    file_lines = listfile.readlines()
    listfile.seek(0)
    for record in file_lines:
        record = record.replace("\n", "")
        if not re.match(str(who), str(record)):
            listfile.write(record + "\n")
    listfile.truncate()
    listfile.close()


file = open('../memcount.txt', 'r')
total_members = int(str(file.readlines()[0]).split('\n')[0])
file.close()
klokky = r.redditor("Klokinator")
messages = r.inbox.messages()
poss_subs = ["Parts", "Patreon", "WritingPrompts", "Updates", "General"]
all_subs = "Parts,Patreon,WritingPrompts,Updates,General"
already_done = []
alreadyin = []

# Open the username list
file = open('../user_list.txt', 'r')

# Add names from a username to a list and post ids to another.
for line in file:
    try:
        name, used = str(line).split(": ")
    except Exception as e:
        line = line.replace("\n", "")
        removel(str(line))
    if name not in alreadyin:
        alreadyin.append(name)
file.close()
otherfile = open('../done.txt', 'r')
for user_line in range(2):
    for line in otherfile:
        linelen = len(line)
        newlinelen = linelen - 1
        if line[:newlinelen] not in already_done:
            already_done.append(line[:newlinelen])
otherfile.close()


def manual_pm(groups_addressed, pm_title, body):
    print("Manual PMing")
    user_list = []
    username_file = open('../user_list.txt', 'r')
    if "All" not in groups_addressed:
        for user_record in username_file:
            has_group = False
            user_full = user_record.replace("\n", "")
            user_name, subscriptions = str(user_full).split(": ")
            for subscription in subscriptions.split(","):
                if not has_group:
                    if subscription in groups_addressed:
                        user_list.append(user_name)
                        has_group = True
    else:
        for user_record in username_file:
            user_name = str(user_record).split(": ")[0]
            user_list.append(user_name)
    username_file.close()
    for user_name in user_list:
        try:
            print(str(user_name))
            r.redditor(user_name).message(pm_title, body)
        except Exception as ex:
            print(ex)
            print(user_name)
            offender_file = open('../offenders.txt', 'a')
            offender_file.write(user_name + "\n")
            offender_file.close()
            torem = user_name + ".*"
            removel(torem)


# For every message in the messages you just fetched:
for message in messages:
    if str(message.id) not in already_done:
        print("Opening message!")
        file = open('../user_list.txt', 'r+')

        # If the message talks about unsubscription, and if the author hasn't already been added and the id isn't done:
        if re.match("unsubscribe.*", str(message.body).lower()) and str(message.author) in alreadyin:
            file.seek(0)
            if len(str(message.body).lower()) > 11:
                try:
                    unsub, args = str(message.body).lower().split(": ")
                    args2 = str(message.body).split(": ")[1]
                    to_reply = "BOT: You've been unsubscribed from: " + args2
                    args = args.split(",")
                    for argument in args:
                        f = open("../user_list.txt", "r+")
                        user_file = f.readlines()
                        f.seek(0)
                        for user_line in user_file:
                            lf = str(message.author) + ": " + ".*"
                            if re.match(lf, user_line):
                                pers, subs = user_line.split(": ")
                                newthing = str(pers) + ": "
                                subs = subs.replace("\n", "")
                                lisargs = subs.split(",")
                                recurred = 0
                                found = 0
                                for lis_argument in lisargs:
                                    if str(lis_argument).lower() == str(argument) and found != 1:
                                        found = 1
                                    elif recurred != 0:
                                        newthing = newthing + "," + lis_argument
                                    else:
                                        newthing = newthing + lis_argument
                                    recurred += 1
                                f.write(newthing + "\n")
                            else:
                                f.write(user_line)
                        f.truncate()
                        f.close()
                    message.reply(to_reply)
                except Exception as e:
                    to_reply = "Sorry, the bot has encountered an error. This error is: \n\n" + str(
                        e) + "\n\n /u/thomas1672 will reply to you in the near future about what went wrong."
                    message.reply(to_reply)
                    to_reply = to_reply + "\n\n" + str(message.author) + "\n\n" + str(message.body)
                    r.redditor("thomas1672").message("error", to_reply)
                    print(e)
                try:
                    f = open("../user_list.txt", "r+")
                    user_file = f.readlines()
                    f.seek(0)
                    for user_line in user_file:
                        lf = str(message.author) + ": " + ".*"
                        if re.match(lf, user_line):
                            pers, subs = user_line.split(": ")
                            if len(subs) > 4:
                                f.write(user_line)
                        else:
                            f.write(user_line)
                    f.truncate()
                    f.close()
                except Exception as e:
                    print(str(e))
                    lin = str(message.author) + ".*"
                    removel(lin)
            else:
                f = open("../user_list.txt", "r+")
                user_file = f.readlines()
                f.seek(0)
                for user_line in user_file:
                    lf = str(message.author) + ": " + ".*"
                    if re.match(lf, user_line):
                        print("Doing nothing!")
                    else:
                        f.write(user_line)
                f.truncate()
                f.close()
                to_reply = "BOT: You've been unsubscribed from all mailing lists!"
                message.reply(to_reply)
                alreadyin.remove(str(message.author))
        elif re.match("subscribe.*", str(message.body).lower()):
            file.seek(0, 2)
            if len(str(message.body).lower()) > 9:
                print("Must be manual!")
                try:
                    sub, args = str(message.body).split(": ")
                    to_reply = "Subscribing you to " + args + "!"
                    arguments = args.split(",")
                    wrong = 0
                    argamount = 0
                    if str(message.author) not in alreadyin:
                        print("not in alreadyin!")
                        towrite = str(message.author) + ": "
                        for arg in arguments:
                            argamount += 1
                            for pos in poss_subs:
                                if arg.lower() != pos.lower():
                                    wrong += 1
                        curwrong = float(wrong) / argamount
                        if curwrong <= 4:
                            towrite = towrite + args
                            alreadyin.append(str(message.author))
                        else:
                            to_reply = to_reply + "\n\nSorry, you could not be subscribed to \"" + arguments + \
                                       "\" because one of them doesn't exist!"
                        file.close()
                        file = open('../user_list.txt', 'a')
                        file.write(towrite + "\n")
                        file.close()
                        file = open('../user_list.txt', 'r+')
                        message.reply(to_reply)
                    else:
                        print("Is in alreadyin!")
                        print("manual sub attempted")
                        f = open("../user_list.txt", "r+")
                        user_file = f.readlines()
                        f.seek(0)
                        lf = str(message.author) + ".*"
                        for user_line in user_file:
                            if re.match(lf, user_line):
                                user_line = user_line.replace("\n", "")
                                pers, subs = str(user_line).split(": ")
                                newthing = str(pers) + ": "
                                lisargs = subs.split(",")
                                recurred = 0
                                for argument in arguments:
                                    wrong = 0
                                    argamount += 1
                                    for pos in poss_subs:
                                        if argument.lower() != pos.lower():
                                            wrong += 1
                                    if wrong <= 4:
                                        if argument not in lisargs:
                                            lisargs.append(argument)
                                    else:
                                        to_reply = to_reply + "\n\nSorry, you could not be " \
                                            "subscribed to \"" + argument + "\" because it doesn't exist! "
                                for arg in lisargs:
                                    print(str(args))
                                    if recurred == 0:
                                        newthing = newthing + arg
                                        recurred = 1
                                    else:
                                        newthing = newthing + "," + arg
                                f.write(newthing + "\n")
                            else:
                                f.write(user_line)
                        f.truncate()
                        f.close()
                        print("replying with " + to_reply)
                        message.reply(to_reply)
                except Exception as e:
                    try:
                        to_reply = "Sorry, the bot has encountered an error. This error is: \n\n" + str(
                            e) + "\n\n /u/thomas1672 will reply to you in the near future about what went wrong."
                        message.reply(to_reply)
                        to_reply = to_reply + "\n\n" + str(message.author) + "\n\n" + str(message.body)
                        r.redditor("thomas1672").message("error", to_reply)
                    except:
                        print(str(e))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
            else:
                print("Simple sub")
                if str(message.author) not in alreadyin:
                    print("not in")
                    towrite = str(message.author) + ": " + all_subs
                    file.close()
                    file = open('../user_list.txt', 'a')
                    file.write(towrite + "\n")
                    file.close()
                    file = open('../user_list.txt', 'r+')
                    to_reply = str(
                        message.author) + ",  you have been subscribed to ALL mailing lists. Message me " \
                                          "'Subscriptions' to find out which ones these are, and 'Unsubscribe [" \
                                          "category],[category2]' to unsubscribe from some, or just 'Unsubscribe' to " \
                                          "unsubscribe from all. "
                    message.reply(to_reply)
                    alreadyin.append(str(message.author))
                else:
                    print("is in")
                    f = open("../user_list.txt", "r+")
                    user_file = f.readlines()
                    f.seek(0)
                    for user_line in user_file:
                        lf = str(message.author) + ".*"
                        if re.match(lf, user_line):
                            pers, subs = user_line.split(": ")
                            newthing = str(pers) + ": " + all_subs + "\n"
                            f.write(newthing)
                        else:
                            f.write(user_line)
                    f.truncate()
                    f.close()
                    to_reply = str(
                        message.author) + ",  you have been subscribed to ALL mailing lists. Message me " \
                                          "'Subscriptions' to find out which ones these are, and 'Unsubscribe [" \
                                          "category],[category2]' to unsubscribe from some, or just 'Unsubscribe' to " \
                                          "unsubscribe from all. "
                    message.reply(to_reply)
            print("Adding someone! - " + str(message.author))
            # Adds their name to the ID list and stuff.
            alreadyin.append(message.author)
        elif re.match("subscriptions.*", str(message.body).lower()) and str(message.author) in alreadyin:
            to_reply = str(message.author) + ", you are subscribed to the following message boards: "
            f = open("../user_list.txt", "r")
            user_file = f.readlines()
            f.close()
            for user_line in user_file:
                lf = str(message.author) + ": " + ".*"
                if re.match(lf, user_line):
                    recurred = 0
                    try:
                        pers, subs = user_line.split(": ")
                        subs = subs.replace("\n", "")
                        newthing = str(pers) + ": "
                        lisargs = subs.split(",")
                        if len(lisargs) >= 1:
                            for lis_argument in lisargs:
                                if recurred == 0:
                                    to_reply = to_reply + lis_argument
                                    recurred = 1
                                else:
                                    to_reply = to_reply + ", " + lis_argument
                        else:
                            to_reply = to_reply + "None!"
                    except Exception as e:
                        to_reply = to_reply + "None!"
                        print(str(e))
            message.reply(to_reply)
        elif str(message.author) == "Klokinator" and str(message.id) not in already_done or str(
                message.author).lower() == "thomas1672" and str(message.id) not in already_done:
            if re.match("\[.*\].*", str(message.subject)):
                groups, title = str(message.subject).split("]")
                groups = groups.replace("[", "")
                sendto = groups.split(",")
                manual_pm(sendto, title, message.body)
                message.reply("Done!")
            else:
                message.reply("No square brackets there..." + "\n\n" + str(message.subject))
        already_done.append(message.id)
        otherfile = open('../done.txt', 'a')
        otherfile.write(str(message.id) + "\n")
        otherfile.close()
        file.close()
# Empty list to prevent double posts.
fixit = []
postreg = "Part [0-9]+.*"


def send_messages(message_type, post):
    keep_going = True
    user_list = []
    post_title = str(post.title)
    username_file = open('../user_list.txt', 'r')
    for username_line in username_file:
        user_name, subscriptions = str(username_line).split(": ")
        if message_type in subscriptions:
            user_list.append(user_name)
    username_file.close()
    if message_type == "Parts":
        part = post_title.split(" ")[1]
        mtitle = "New Part!"
        mtext = "New Part on /r/TheCryopodToHell! - [Part " + str(
            part) + "](" + post.permalink + ")\n\n" + "To unsubscribe from these types of messages, click [here](" \
            "https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=Unsubscribe%3A+Parts)! "
    elif message_type == "Patreon":
        mtitle = "New Patreon Post!"
        mtext = "New Patreon Post on /r/TheCryopodToHell! - [" + post_title + "](" + post.permalink + ")\n\n" + \
                "To unsubscribe from these types of messages, click " \
                "[here](https://np.reddit.com/message/compose/?to=CryopodBot" \
                "&subject=unsubscribe&message=Unsubscribe%3A+Patreon)! "
    elif message_type == "WritingPrompts":
        mtitle = "New WritingPrompts Response!"
        mtext = "New WritingPrompts Response on /r/TheCryopodToHell! - [" + post_title + "](" + post.permalink + \
                ")\n\n" + "To unsubscribe from these types of messages, click [here]" \
                "(https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&" \
                "message=Unsubscribe%3A+WritingPrompts)!"
    elif message_type == "Updates":
        mtitle = "New Updates Post!"
        mtext = "New Update Post on /r/TheCryopodToHell! - [" + post_title + "](" + post.permalink + ")\n\n" + \
                "To unsubscribe from these types of messages, click [here](https://np.reddit.com/message/compose/?to=" \
                "CryopodBot&subject=unsubscribe&message=Unsubscribe%3A+Updates)!"
    elif message_type == "General":
        mtitle = "New Post!"
        mtext = "New Post from Klok on /r/TheCryopodToHell! - [" + post_title + "](" + post.permalink + ")\n\n" + \
                "To unsubscribe from these types of messages, click [here](https://np.reddit.com/message/compose/?to=" \
                "CryopodBot&subject=unsubscribe&message=Unsubscribe%3A+General)!"
    else:
        keep_going = False
        mtitle = ""
        mtext = ""
    if keep_going:
        for user_name in user_list:
            try:
                r.redditor(user_name).message(mtitle, mtext)
            except Exception as ex:
                print(ex)
                print(user_name)
                offender_file = open('../offenders.txt', 'r+')
                offender_file.write(user_name + "\n")
                offender_file.close()
                torem = user_name + ".*"
                removel(torem)


# For thread in the subreddit, out of the newest thread.
for submission in subreddit.get_new(limit=1):
    print("Checking for submission")
    print(str(submission.title))
    time.sleep(3)
    # Set variables to prevent annoying the reddit api.
    author = submission.author
    title = str(submission.title)
    sub_id = str(submission.id)
    # Same as message checking but for threads.
    file = open('../parts.txt', 'r+')
    for line in file:
        linelen = len(line)
        newlinelen = linelen - 1
        if line[:newlinelen] not in fixit:
            fixit.append(line[:newlinelen])
    # If the author is Klok and it begins with part, do this:
    if re.match(postreg, title):
        print("Matched?")
    if sub_id not in fixit:
        print("no id?")
    if str(author).lower() == "klokinator" and re.match(postreg, title) and sub_id not in fixit or str(
            author).lower() == "thomas1672" and re.match("Test.*", title) and sub_id not in fixit:
        print("we matched fine")
        file.write(sub_id + "\n")
        file.close()
        fixit.append(str(sub_id))
        sub_type = "Parts"
        with open('../lastpart.txt', 'r') as file:
            lastprt = file.readline()
        file.close()
        alreadyin = []
        finished = []
        todo = []
        nxtparts = r.submission(id = lastprt)
        nxtpart = nxtparts.comments[0]
        bodtext = nxtpart.body
        bodytext = bodtext.replace(
            "\n\n***\n\n[^^Bot ^^Commands](https://github.com/TGWaffles/cryopodbot/wiki/Reddit-Bot-Information) ^^| ["
            "^^Bot ^^made ^^by ^^/u/thomas1672!](http://reddit.com/u/thomas1672) ^^| [^^Donate ^^to ^^the ^^bot!]("
            "https://www.patreon.com/tgwaffles)",
            "")
        add = nxtpart.body[:-228] + "\n" + "\n" + "**[" + submission.title + "](" + submission.permalink + ")**" + "\n\n" \
                                                                                                            "***\n\n[" \
                                                                                                            "^^Bot " \
            "^^Commands]" \
            "(https://github.com/TGWaffles/cryopodbot/wiki/Reddit-Bot-Information) ^^| [^^Bot ^^made ^^by ^" \
            "^/u/thomas1672!](http://reddit.com/u/thomas1672) ^^| [^^Donate ^^to ^^the ^^bot!]" \
            "(https://www.patreon.com/tgwaffles) "
        nxtpart.edit(add)
        prevurl = nxtpart.submission.permalink
        uwc = []
        wc = 0
        for user_line in str(submission.selftext).split():
            if user_line not in uwc:
                wc += 1
                uwc.append(user_line)
        postedcomment = submission.add_comment(
            "Hi. I'm a bot, bleep bloop." + "\n" + "\n" + "\n" + "\n" + "If you want to chat"
            " with " + str(total_members) +
            " fellow Cryopod readers, join the Discord at https://discord.gg/6JtsQJR" + "\n" + "\n" +
            "\n" + "[Click Here to be PM'd new updates!](https://np.reddit.com/message/compose/?to=CryopodBot"
            "&subject=Subscribe&message=Subscribe) " + "[Click Here to unsubscribe!](https://np.reddit.com/"
            "message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)" + "\n" + "\n" +
            "\n" + "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, but be sure to "
            "mark it as a gift or Paypal takes 10%. " + "\n" + "\n" + "Patreon can also be pledged to [here!]("
            "https://www.patreon.com/klokinator)" +
            "\n" + "\n" + "This part consisted of: " + str(len(submission.selftext)) +
            " characters, " + str(len(str(submission.selftext).split())) +
            " words, and " + str(wc) +
            " unique words!" + "\n" + "\n" + "[" + "Previous Part" + "](" + prevurl + ")" + "\n\n***\n\n[^^Bot"
            " ^^Commands](https://github.com/TGWaffles/cryopodbot/wiki/Reddit-Bot-Information) ^^| [^^Bot ^^made ^^by "
            "^^/u/thomas1672!](http://reddit.com/u/thomas1672) ^^| [^^Donate ^^to ^^the ^^bot!]"
            "(https://www.patreon.com/tgwaffles)")
        file = open('../lastpart.txt', 'w')
        file.write(str(postedcomment.permalink))
        file.close()
        submission.set_flair("STORY", "story")
        # Sticky the comment that was just posted.
        postedcomment.distinguish(sticky=True)
        # Get the index list's ID.
        toedit = r.submission(id = '56tvbw')
        time.sleep(2)
        # Add post that was just posted to the index list.
        tempedit = toedit.selftext
        putin = tempedit + "\n" + "\n" + "[" + submission.title + "](" + submission.short_link + ")"
        time.sleep(2)
        toedit.edit(putin)
        time.sleep(2)
        if title[0:4].lower() != "test":
            manual_pm(['Parts'], "New Part on /r/TheCryopodToHell!",
                      "[" + submission.title + "](" + submission.short_link + ")")
    # If it's not a part, check if it's a patreon post, an update, or a general klok post
    elif (re.match(".*\[.*Patreon.*\].*", title) and str(submission.author).lower() == "klokinator" and
            sub_id not in fixit):
        file.write(sub_id + "\n")
        file.close()
        fixit.append(str(sub_id))
        sub_type = "Patreon"
        send_messages(sub_type, submission)
    elif (re.match(".*\[.*Update.*\].*", title) and str(submission.author).lower() == "klokinator" and
            sub_id not in fixit):
        file.write(sub_id + "\n")
        file.close()
        fixit.append(str(sub_id))
        sub_type = "Updates"
        send_messages(sub_type, submission)
    # elif str(submission.author).lower() == "klokinator" and id not in fixit:
    # file.write(id + "\n")
    # file.close()
    # fixit.append(str(id))
    # type = "General"
    # send_messages(type,submission)
    else:
        file.close()
# Gets all comments in the subreddit, then flattens them.
subreddit_comments = subreddit.get_comments()
subcomments = praw.helpers.flatten_tree(subreddit_comments)
# Loops through every comment in the sub.
for comment in subcomments:
    # Opens file with comment ids.
    otherfile = open('../done.txt', 'r+')
    # Do it twice to make sure.
    for user_line in range(2):
        for line in otherfile:
            linelen = len(line)
            newlinelen = linelen - 1
            if line[:newlinelen] not in already_done:  # just line[:-1], srsly
                already_done.append(line[:newlinelen])
    # If someone's tagging us and we've not processed their comment:
    if "/u/cryopodbot" in str(comment.body).lower() and str(comment.id) not in already_done:
        # If it's talking about the post, comment the post.
        if "post" in str(comment.body).lower():
            # Make sure the bot doesn't respond to itself.
            if str(comment.author).lower() != "cryopodbot":
                # Reply!
                comment.reply(
                    "Hi. I'm a bot, bleep bloop." + "\n" + "\n" + "If you're about to post regarding a typo and this "
                    "Part was just posted, please wait ten minutes, "
                    "refresh, and then see if it's still there!" + "\n" +
                    "\n" + "Also, if you want to report typos anywhere, please respond to this bot to keep the main "
                    "post clutter free. Thank you!" + "\n" + "\n" + "\n" + "[Click Here to be PM'd new "
                    "updates!](https://np.reddit.com/message/compose/?to=CryopodBot&subject"
                    "=Subscribe&message=Subscribe) " + "[Click Here to unsubscribe!](https://np.reddit.com/"
                    "message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)" + "\n" + "\n" +
                    "\n" + "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, "
                    "but be sure to mark it as a gift or Paypal takes 10%. " + "\n" + "\n" + "Patreon can also be "
                    "pledged to [here!](https://www.patreon.com/klokinator)")
                # Post the ID to a file to prevent duplicates.
                otherfile.write(str(comment.id) + "\n")
        # If the post wants a flair and it's me or Klok:
        elif "flair info" in str(comment.body).lower():
            if str(comment.author).lower() == "thomas1672" or str(comment.author).lower() == "klokinator":
                flairsubmtoset: Submission = r.submission(id = str(comment.parent_id)[-6:])
                # Flair and stop duplicate flairing (would only waste processor time)
                flairsubmtoset.flair("INFO", "info")
                otherfile.write(str(comment.id) + "\n")
        elif "flair question" in str(comment.body).lower():
            if str(comment.author).lower() == "thomas1672" or str(comment.author).lower() == "klokinator":
                flairsubmtoset = r.submission(id = str(comment.parent_id)[-6:])
                flairsubmtoset.flair("QUESTION", "question")
                otherfile.write(str(comment.id) + "\n")
        elif str(comment.author).lower() != "cryopodbot":
            select = int(random.randint(0, 10))
            if select == 1:
                comment.reply("You called? ;)")
            elif select == 2:
                comment.reply("What's up?")
            elif select == 3:
                comment.reply("Hey!")
            elif select == 4:
                comment.reply("Go check out my GitHub Repository at https://github.com/TGWaffles/cryopodbot")
            elif select == 5:
                comment.reply(
                    "Tagging me in a post can trigger specific things. One of the random replies means I didn't "
                    "understand what you asked!")
            elif select == 6:
                comment.reply("Yo, 'sup?")
            elif select == 7:
                comment.reply("Go check out Klok's patreon [here!](https://www.patreon.com/klokinator)")
            elif select == 8:
                comment.reply("I was coded by /u/thomas1672 - direct all questions to him!")
            elif select == 9:
                comment.reply("Now taking suggestions for more of these random replies in the discord!")
            else:
                comment.reply("Join the discord @ https://discord.gg/EkdeJER")
            otherfile.write(str(comment.id) + "\n")
# Re-Save the file.
otherfile.close()
