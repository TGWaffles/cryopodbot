footer = ("\n\n"
          "***"
          "\n\n"
          "[^^Bot ^^Commands](https://github.com/TGWaffles/cryopodbot/wiki/Reddit-Bot-Information) "
          "^^| "
          "[^^Bot ^^made ^^by ^^/u/thomas1672!](http://reddit.com/u/thomas1672) "
          "^^| "
          "[^^Donate ^^to ^^the ^^bot!](https://www.patreon.com/tgwaffles)")

replystr = ("Hi. I'm a bot, bleep bloop."
            "\n\n\n\n"
            "If you want to chat with {totalmemb} fellow Cryopod readers, "
            "join the Discord at https://discord.gg/6JtsQJR"
            "\n\n\n"
            "[Click Here to be PM'd new updates!]"
            "(https://np.reddit.com/message/compose/?to=CryopodBot&subject=Subscribe&message=Subscribe) "
            "[Click Here to unsubscribe!]"
            "(https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)"
            "\n\n\n"
            "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, "
            "but be sure to mark it as a gift or Paypal takes 10%. "
            "\n\n"
            "Patreon can also be pledged to [here!](https://www.patreon.com/klokinator)"
            "\n\n"
            "This part consisted of: {chars} characters, {words} words, and {uwords} unique words!"
            "\n\n"
            "[Previous Part]({prevurl})") + footer

replystr2 = ("Hi. I'm a bot, bleep bloop."
             "\n\n"
             "If you're about to post regarding a typo and this Part was just posted, please wait ten minutes, refresh,"
             " and then see if it's still there!"
             "\n\n"
             "Also, if you want to report typos anywhere, please respond to this bot to keep the main post clutter "
             "free. Thank you!"
             "\n\n\n"
             "[Click Here to be PM'd new updates!]"
             "(https://np.reddit.com/message/compose/?to=CryopodBot&subject=Subscribe&message=Subscribe) "
             "[Click Here to unsubscribe!]"
             "(https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)"
             "\n\n\n"
             "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, but be sure to mark it as"
             " a gift or Paypal takes 10%. "
             "\n\n"
             "Patreon can also be pledged to [here!](https://www.patreon.com/klokinator)")

footer2 = ("\n\n"
     "**"
     "[{title}]({permalink})"
     "**"
     "\n\n"
     "***"
     "\n\n"
     "[^^Bot ^^Commands](https://github.com/TGWaffles/cryopodbot/wiki/Reddit-Bot-Information)"
     " ^^| "
     "[^^Bot ^^made ^^by ^^/u/thomas1672!](http://reddit.com/u/thomas1672)"
     " ^^| "
     "[^^Donate ^^to ^^the ^^bot!](https://www.patreon.com/tgwaffles)")

pmtitle = {
    'Parts': "New Part!",
    'Patreon': "New Patreon Post!",
    'WritingPrompts': 'New WritingPrompts Response!',
    'Updates': 'New Updates Post!',
    'General': 'New Post!'
}

pmbody = {
    'Parts': ("New Part on /r/TheCryopodToHell! - [Part {part}]({permalink})"
              "\n\n"
              "To unsubscribe from these types of messages, click "
              "[here](https://np.reddit.com/message/compose/?to=CryopodBot&"
              "subject=unsubscribe&message=Unsubscribe%3A+Parts)! "),

    'Patreon': ("New Patreon Post on /r/TheCryopodToHell! - [{title}]({permalink})"
                "\n\n"
                "To unsubscribe from these types of messages, click "
                "[here](https://np.reddit.com/message/compose/?to=CryopodBot"
                 "&subject=unsubscribe&message=Unsubscribe%3A+Patreon)! "),

    'WritingPrompts': ("New WritingPrompts Response on /r/TheCryopodToHell! - [{title}]({permalink})"
                       "\n\n"
                       "To unsubscribe from these types of messages, click "
                       "[here](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe"
                       "&message=Unsubscribe%3A+WritingPrompts)!"),

    'Updates': ("New Update Post on /r/TheCryopodToHell! - [{title}]({permalink})"
                "\n\n"
                "To unsubscribe from these types of messages, click "
                "[here](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe"
                "&message=Unsubscribe%3A+Updates)!"),

    'General': ("New Post from Klok on /r/TheCryopodToHell! - [{title}]({permalink)"
                "\n\n"
                "To unsubscribe from these types of messages, click "
                "[here](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe"
                "&message=Unsubscribe%3A+General)!")
}

pm_unsub = ("BOT: You've been unsubscribed!")

pm_sub = ("BOT: Thanks, you've been added to the list!")

randreply = [
    ("You called? ;)"),
    ("What's up?"),
    ("Hey!"),
    ("Go check out my GitHub Repository at https://github.com/TGWaffles/cryopodbot"),
    ("Tagging me in a post can trigger specific things. "
     "One of the random replies means I didn't understand what you asked!"),
    ("Yo, 'sup?"),
    ("Go check out Klok's patreon [here!](https://www.patreon.com/klokinator)"),
    ("I was coded by /u/thomas1672 - direct all questions to him!"),
    ("Now taking suggestions for more of these random replies in the discord!")
]

randdef = ("Join the discord @ https://discord.gg/EkdeJER")
