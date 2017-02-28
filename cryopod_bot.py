#!/usr/bin/python
import logging
import praw
import random
import time

from pw_bot import *
from common_util import *

def set_up_reddit():
    user_agent = "CryoBot 1.0"
    reddit = praw.Reddit(user_agent = user_agent)
    reddit.login(REDDIT_USERNAME, REDDIT_PASSWORD, disable_warning=True)
    return reddit

def process_subscription_messages(reddit):
    messages = reddit.get_messages()
    subscribed_users = unique_file_lines(SUBSCRIBED_USERS_FILE)
    processed_ids = unique_file_lines(PROCESSED_IDS_FILE)

    for message in messages:
        print "Opening message!"
        author = unicode(message.author).encode("ascii", "ignore")
        message_id = unicode(message.id).encode("ascii", "ignore")

        if is_processed_id(message_id, processed_ids):
            continue

        # note: message ids that are neither subscribe/unsubscribe
        #       are not added to the processed message id file
        if is_unsubscribe_request(message) and \
           is_subscribed(message.author, subscribed_users):
                try:
                    subscribed_users.remove(author)
                    overwrite_file(SUBSCRIBED_USERS_FILE, "\n".join(subscribed_users))
                    message.reply("BOT: You've been unsubscribed!")
                    processed_ids.add(message_id)
                    overwrite_file(PROCESSED_IDS_FILE, "\n".join(processed_ids))
                except Exception as e:
                    print e
                time.sleep(2)
                print message_id
                print "unsubscribed reply sent"

        elif is_subscribe_request(message) and \
             not is_subscribed(author, subscribed_users):
                print "Adding someone! - " + author
                try:
                    subscribed_users.add(author)
                    overwrite_file(SUBSCRIBED_USERS_FILE, "\n".join(subscribed_users))
                    message.reply("BOT: Thanks, you've been added to the list!")
                    processed_ids.add(message_id)
                    overwrite_file(PROCESSED_IDS_FILE, "\n".join(processed_ids))
                except Exception as e:
                    print e
                time.sleep(2)
                print message_id
                print "unsubscribed reply sent"

    overwrite_file(SUBSCRIBED_USERS_FILE, "\n".join(subscribed_users))
    overwrite_file(PROCESSED_IDS_FILE, "\n".join(processed_ids))

# Only gets the first page of r/TheCryopodToHell/comments
# presumably this gets run often enough that this is okay
def process_tagged_comments(reddit):
    subreddit = reddit.get_subreddit("thecryopodtohell")
    subreddit_comments = subreddit.get_comments()
    subcomments = praw.helpers.flatten_tree(subreddit_comments)
    processed_ids = unique_file_lines(PROCESSED_IDS_FILE)

    for comment in subcomments:
        if is_bot_tagged(comment) and \
           not is_author(BOT_USERNAME, comment) and \
           not is_processed_id(comment.id, processed_ids):

                comment_id = unicode(comment.id).encode("ascii", "ignore")
                submission_id = unicode(comment.parent_id).encode("ascii", "ignore")[-6:]

                # If it's talking about the post, comment the post.
                if is_post_about("post", comment):
                    comment.reply(BOT_POST_COMMENT_RESPONSE)
                    print "placeholder"

                #If the post wants a flair and it's me or Klok:
                elif is_post_about("flair info", comment) and \
                     (is_author(TOM_USERNAME, comment) or \
                      is_author(KLOK_USERNAME, comment)):
                        #Flair and stop duplicate flairing (would only waste processor time)
                        flairsubmtoset = reddit.get_submission(submission_id=submission_id)
                        flairsubmtoset.set_flair("INFO", "info")

                elif is_post_about("flair question", comment) and \
                     (is_author(TOM_USERNAME, comment) or \
                      is_author(KLOK_USERNAME, comment)):
                        flairsubmtoset = reddit.get_submission(submission_id=submission_id)

                # Every other comment tagging the bot, just say some message
                else:
                    response = random.choice(BOT_TAGGED_RESPONSES)
                    comment.reply(response)

                # mark the comment processed and write the file to disk
                processed_ids.add(comment_id)
                overwrite_file(PROCESSED_IDS_FILE, "\n".join(processed_ids))

def process_submissions(reddit):
    subreddit = reddit.get_subreddit("thecryopodtohell")
    webseries_parts_ids = unique_file_lines(ALL_WEBSERIES_PART_IDS_FILE)

    #For thread in the subreddit, out of the newest thread.
    for submission in subreddit.get_new(limit=1):
        time.sleep(3)

        submission_id = unicode(submission.id).encode("ascii", "ignore")

        if (is_author(KLOK_USERNAME, submission) and \
            is_webseries_part(submission) and \
            not is_processed_webseries_part(submission_id, webseries_parts_ids)) or \
           (is_author(TOM_USERNAME, submission) and \
            is_test_webseries_part(submission) and \
            not is_processed_webseries_part(submission_id, webseries_parts_ids)):
                webseries_parts_ids.add(submission_id)
                overwrite_file(ALL_WEBSERIES_PART_IDS_FILE, "\n".join(webseries_parts_ids))

                link_previous_part_to_latest(reddit, submission)

                posted_bot_comment = post_bot_first_comment(reddit, submission)
                posted_bot_comment = unicode(posted_bot_comment).encode("ascii", "ignore")
                overwrite_file(LATEST_BOT_STICKY_COMMENT_FILE, posted_bot_comment)
                submission.set_flair("STORY", "story")

                link_index_list_to_latest(reddit, submission)

                if not is_test_webseries_part(submission):
                    notify_subscribed_users(submission)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit = set_up_reddit()

    process_subscription_messages(reddit)
    process_tagged_comments(reddit)
    process_submissions(reddit)


