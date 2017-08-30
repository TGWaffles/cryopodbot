#!/usr/bin/python
import praw
import sqlite3
#Imports all passwords from a hidden file ;)
from pw_bot import *

class SubmissionManager:
    """
    Manages the statistics table
    entries in the story are marked as isStory = 1
    """
    reddit = None
    subreddit = None
    cursor = None
    def __init__(self, cursor):
        self.cursor = cursor
        self.create_statistics_table()

    def create_statistics_table(self):
        self.cursor.execute("create table if not exists statistics" \
            "(id text," \
            "url text," \
            "title text," \
            "author text," \
            "selftext text," \
            "score int," \
            "createddate int)")

        columns = [col[1] for col in self.do_query("PRAGMA table_info(statistics)")]

        def addStatCol(column,colType):
            if column in columns:
                return
            self.cursor.execute("ALTER TABLE statistics ADD COLUMN " + column + " " + colType)

        addStatCol("wordCount","int")
        addStatCol("charCount","int")
        addStatCol("isStory","int")

    def connect_to_reddit(self):
        if self.reddit is not None:
            return

        self.reddit= praw.Reddit(client_id=REDDIT_CLIENT_ID,
                             client_secret=REDDIT_CLIENT_SECRET,
                             password=REDDIT_PASS,
                             user_agent=REDDIT_USER_AGENT,
                             username=REDDIT_USERNAME)

        self.subreddit = self.reddit.get_subreddit("TheCryopodToHell")

    def get_reddit_submissions(self, submissionLimit = 5):
        self.connect_to_reddit()

        if int(self.do_query("select count(1) from statistics")[0][0]) == 0:
            #if nothing in the database try to get everything
            submissionLimit = 1000

        for submission in self.subreddit.get_new(limit=submissionLimit):
            #print(dir(submission))
            item =[str(submission.id),
                   str(submission.url),
                   str(submission.title),
                   str(submission.author),
                   str(submission.selftext),
                   int(submission.score),
                   int(submission.created_utc)]

            #print("loaded item from reddit: " +item[0])
            if int(self.do_query("select count(1) from statistics where id = '"+item[0]+"'")[0][0]) > 0:
                #dont add items already added
                continue

            self.cursor.execute("insert into statistics "
                      "(id,url,title,author,selftext,score,createddate) "
                      "values(?,?,?,?,?,?,?)"
                      ,item)
            #print("added item to db: " +item[0])
        self.set_is_story()
        self.set_word_counts()

    def update_reddit_submission_scores(self, submissionLimit = 5):
        """
        Score can change with time so this repulls the scores to keep the stats up to date
        """
        self.connect_to_reddit()

        for submission in self.subreddit.get_new(limit=submissionLimit):
            id = str(submission.id)
            score = int(submission.score)

            if int(self.do_query("select count(1) from statistics where id = '"+id+"'")[0][0]) == 0:
                #if we dont have this submission already try to load any missing ones
                self.get_reddit_submissions(submissionLimit)

            self.cursor.execute("update statistics "
                      "set score = ? "
                      "where id = ?"
                      ,[score,id])
            #print("updated score. item: " +id+" score: "+str(score))

    def set_is_story(self):
        self.cursor.execute("update statistics "
                  "set isStory = case when author = 'Klokinator' and title like 'Part%' then 1 else 0 end "
                  "where isStory is null")

    def set_word_counts(self):
        for row in self.do_query("select rowid,selftext from statistics where wordCount is null"):
            words = row[1].split()
            wordCount = len(words)
            charCount = sum([len(word) for word in words])
            self.cursor.execute("update statistics set wordCount=?,charCount=? where rowid=?",[wordCount,charCount,row[0]])

    def do_query(self, queryText):
        self.cursor.execute(queryText)
        return self.cursor.fetchall()

    def get_stats(self):
        return self.do_query("select 'All',count(1) ,sum(wordCount),sum(charcount),sum(score) from statistics where isstory = 1")

    def get_weekly_stats(self):
        sept_12_2016 = 1473638400
        week = "(createddate-" + str(sept_12_2016) + ")/(3600*24*7)"
        # this finds the stats on a per week basis
        return self.do_query("select 1+" + week + ","
                                "count(1),"
                                "sum(wordCount),"
                                "sum(charcount),"
                                "sum(score) "
                                "from statistics "
                                "where isstory =1 group by " + week +
                                "order by " + week + " asc")

def p(queryResult):
    for row in queryResult:
        print(row)

try:
    conn = sqlite3.connect('statistics.db')
    submissions = SubmissionManager(conn.cursor())
    #this will get new submissions and also update scores for existing submissions
    submissions.update_reddit_submission_scores()
    conn.commit()

    print("(week, parts, word count, char count, score)")
    p(submissions.get_stats())
    p(submissions.get_weekly_stats())

    #p(submissions.do_query("select title,wordCount,charCount from statistics where isStory = 1"))
    #p(submissions.do_query("select rowid,title from statistics where isstory = 1"))

except Exception as ex:
    print(ex.with_traceback())
finally:
    conn.close()