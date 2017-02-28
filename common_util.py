#!/usr/bin/python
import time

BOT_USERNAME = "cryopodbot"
TOM_USERNAME = "thomas1672"
KLOK_USERNAME = "klokinator"
SUBSCRIBED_USERS_FILE = "list.txt"
PROCESSED_IDS_FILE = "done.txt"
ALL_WEBSERIES_PART_IDS_FILE = "parts.txt"
LATEST_BOT_STICKY_COMMENT_FILE = "lastpart.txt"
INDEX_LIST_POST_ID = "56tvbw"
OFFENDERS_FILE = "offenders.txt"

MESSAGE_BOT_LINK = "https://np.reddit.com/message/compose/?to=CryopodBot"
SUBSCRIBE_LINK = MESSAGE_BOT_LINK + "&subject=Subscribe&message=Subscribe"
UNSUBSCRIBE_LINK = MESSAGE_BOT_LINK + "&subject=unsubscribe&message=unsubscribe"
PAYPAL_EMAIL = "Klokinator@yahoo.com"
PATREON_LINK = "https://www.patreon.com/klokinator"
FOOTER_MESSAGE = """\
[Click Here to be PM'd new updates!] (%(sub_link)s)\
[Click Here to unsubscribe!] (%(unsub_link)s)\n\n\n\
If you want to donate to Klokinator, send paypal gifts to %(paypal_email)s, \
but be sure to mark it as a gift or Paypal takes 10 percent.\n\n\
Patreon can also be pledged to [here!] (%(patreon_link)s)\n\n\
""" % dict(sub_link=SUBSCRIBE_LINK, unsub_link=UNSUBSCRIBE_LINK,
           paypal_email=PAYPAL_EMAIL, patreon_link=PATREON_LINK)

BOT_POST_COMMENT_RESPONSE = """\
Hi. I'm a bot, bleep bloop.\n\n\ If you're about to post regarding a typo and this Part was just posted, \
please wait ten minutes, refresh, and then see if it's still there!\n\n\
Also, if you want to report typos anywhere, please respond to this bot to \
keep the main post clutter free. Thank you!\n\n\n\
""" + FOOTER_MESSAGE

# why are there TWO discord links??

BOT_TAGGED_RESPONSES = [\
    "You called? ;),", "What's up?", "Hey!", "Yo, 'sup?",
    "Go check out my discord at https://github.com/TGWaffles/cryopodbot",
    "Tagging me in a post can trigger specific things. " + \
    "One of the random replies means I didn't understand what you asked!",
    "Go check out Klok's patreon [here!] (" + PATREON_LINK + ")",
    "I was coded by /u/thomas1672 - direct all questions to him!",
    "Now taking suggestions for more of these random supplies in the discord!",
    "Join the discord @ https://discord.gg/EkdeJER"]

BOT_FIRST_COMMENT_RESPONSE = """\
Hi. I'm a bot, bleep bloop.\n\n\n\n\
If you want to chat with 200+ fellow Cryopod readers, \
join the Discord at https://discord.gg/6JtsQJR\n\n\n""" + FOOTER_MESSAGE + \
"""\
This part consisted of: %(char_count)s characters, %(word_count)s words, and \
%(unique_word_count)s unique words!\n\n\
[Previous Part] (%(prev_url)s)"""

NEW_POST_MESSAGE = "New Post on /r/TheCryopodToHell! - [%(title)s](%(post_link)s)"

def unique_file_lines(file_name):
    unique_contents = set()
    file_handle = open(file_name, "r")
    for line in file_handle:
        unique_contents.add(line.strip())
    file_handle.close()
    return unique_contents

def is_unsubscribe_request(message):
    ascii_message = unicode(message.body).lower().encode("ascii", "ignore")
    return "unsubscribe" in ascii_message

def is_subscribe_request(message):
    ascii_message = unicode(message.body).lower().encode("ascii", "ignore")
    return "subscribe" in ascii_message

def is_subscribed(user, subscribed_users):
    ascii_user = unicode(user).lower().strip().encode("ascii", "ignore")
    return ascii_user in subscribed_users

def is_processed_id(object_id, processed_ids):
    ascii_object_id = unicode(object_id).strip().encode("ascii", "ignore")
    return ascii_object_id in processed_ids

def overwrite_file(file_name, file_contents):
    file_handle = open(file_name, "w")
    file_handle.write(file_contents + "\n")
    file_handle.close()

def is_bot_tagged(comment):
    ascii_comment = unicode(comment.body).lower().strip().encode("ascii", "ignore")
    return "/u/cryopodbot" in ascii_comment

def is_post_about(keyword, comment):
    ascii_comment = unicode(comment.body).lower().strip().encode("ascii", "ignore")
    return keyword in ascii_comment

def is_author(username, comment):
    ascii_author = unicode(comment.author).lower().encode("ascii", "ignore")
    return username == ascii_author

def is_webseries_part(submission):
    ascii_title = unicode(submission.title).lower().encode("ascii", "ignore")
    return ascii_title[0:4] == "part"

def is_test_webseries_part(submission):
    ascii_title = unicode(submission.title).lower().encode("ascii", "ignore")
    return ascii_title[0:4] == "test"

def is_processed_webseries_part(submission_id, processed_parts):
    return submission_id.encode("ascii", "ignore") in processed_parts

def get_latest_bot_sticky_comment_url():
    sticky_url_file = open(LATEST_BOT_STICKY_COMMENT_FILE, "r")
    sticky_url = sticky_url_file.readline()
    sticky_url_file.close()
    return sticky_url

def link_previous_part_to_latest(reddit, submission):
    # update previous webseries part's bot comment to link to this
    latest_sticky_url = get_latest_bot_sticky_comment_url()
    latest_sticky_comment_obj = reddit.get_submission(latest_sticky_url)

    # this is a risky assumption if somebody ever beats the bot
    latest_sticky_comment = latest_sticky_comment_obj.comments[0]
    updated_comment = latest_sticky_comment.body + "\n\n" + \
                      "**[" + submission.title + "]" + \
                      "(" + submission.permalink + ")**"

    latest_sticky_comment_obj.edit(updated_comment)

def format_bot_first_comment(reddit, submission):
    latest_sticky_url = get_latest_bot_sticky_comment_url()
    latest_sticky_comment_obj = reddit.get_submission(latest_sticky_url)

    latest_part_id = latest_sticky_comment_obj.comments[0].parent_id
    latest_part = reddit.get_info(thing_id=latest_part_id)
    latest_part_url = latest_part.permalink

    submission_words = submission.selftext.split()
    char_count = len(submission.selftext)
    word_count = len(submission_words)
    unique_word_count = len(set(submission_words))

    bot_first_comment = BOT_FIRST_COMMENT_RESPONSE % dict(\
                            char_count=char_count,
                            word_count=word_count,
                            unique_word_count=unique_word_count,
                            prev_url=latest_part_url)
    return bot_first_comment

def post_bot_first_comment(reddit, submission):
    bot_comment = format_bot_first_comment(reddit, submission)
    posted_bot_comment = submission.add_comment(bot_first_comment)
    posted_bot_comment.distinguish(sticky=True)
    return posted_bot_comment

def link_index_list_to_latest(reddit, submission):
    #Get the index list's ID.
    index_list_post = reddit.get_submission(submission_id=INDEX_LIST_POST_ID)
    time.sleep(2)

    #Add post that was just posted to the index list.
    updated_index_list_post = index_list_post.selftext + "\n\n" + \
                              "[" + submission.title + "]" + \
                              "(" + submission.permalink + ")"
    time.sleep(2)

    index_list_post.edit(updated_index_list_post)
    time.sleep(2)

def record_user_as_offender(username):
    print(username)
    offenders_file = open(OFFENDERS_FILE, "r+")
    offenders_file.write(username + "\n")
    offenders_file.close()

def notify_subscribed_users(submission):
    #Put all users in the username file into a list, then:
    subscribed_users = unique_file_lines(SUBSCRIBED_USERS_FILE)
    notified_users = []

    new_post_message = NEW_POST_MESSAGE % dict(\
                        title=submission.title,
                        post_link=submission.permalink)

    #For every name in the list, send them this message with the link to the part.
    for subscribed_user in subscribed_users:
        try:
            reddit.send_message(subscribed_user, "New Post!", new_post_message)
            notified_users.append(subscribed_user)
        except Exception as ex:
            print(ex)
            record_user_as_offender(subscribed_user)
        time.sleep(1)
    time.sleep(10)


    failed_users = [user for user in subscribed_users if user not in notified_users]
    for failed_user in failed_users:
        try:
            print placeholder
            reddit.send_message(subscribed_user, "New Post!", new_post_message)
        except Exception as ex:
            print(ex)
            record_user_as_offender(failed_user)
            subscribed_users.remove(failed_user)
            ovewrite_file(SUBSCRIBED_USERS_FILE, "\n".join(subscribed_users))
        time.sleep(1)


