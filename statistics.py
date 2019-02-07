#!/usr/bin/env python3
import collections
import json
from prettytable import PrettyTable


class Statistics(object):
    """ Computes summary statistics of a query (i.e. text, screen names, and hashtags)

    Variables:
        tweet_nested_list (list) : nested list of twitter search results (json)
        texts (list): list of all tweets
        hashtags (list): list of all hashtags
        screen_names (list): list of all screen names
        words (list): list of words in tweets
    """
    def __init__(self, tweet_nested_list):
        self.tweet_nested_list = tweet_nested_list
        self.texts = []
        self.screen_names = []
        self.hashtags = []
        self.words = []
        # method calls
        self.get_texts()
        self.get_hashtags()
        self.get_screen_names()
        self.get_words()

    def get_texts(self):
        """Iterates over the nested json list and appends tweets (statuses) to instance list

        """
        self.texts = [status['text']
                        for my_dict in self.tweet_nested_list
                            for status in my_dict['statuses']]

    def get_hashtags(self):
        """Iterates over the nested json list and appends hashtags to instance list

        """
        self.hashtags = [hashtag['text']  # get text value
                         for my_dict in self.tweet_nested_list  # iterate over each list of 100 tweets in nested list
                            for status in my_dict['statuses']  # iterate over each status in dictionary
                                for hashtag in status['entities']['hashtags']  # iterate over each hashtag in nested dict
                         ]

    def get_screen_names(self):
        """Iterates over the nested json list and appends screen name to instance list

        """
        self.screen_names = [user_mention.get('screen_name')
                             for my_dict in self.tweet_nested_list
                                for status in my_dict['statuses']
                                    for user_mention in status['entities']['user_mentions']
                             ]

    def get_words(self):
        """Iterates over the nested json list and appends all words from tweets to instance list

        """
        self.words = [word
                        for my_dict in self.tweet_nested_list
                            for status in my_dict['statuses']
                                for word in status['text'].split()
                      ]

    def print_prettytable(self):
        """Iterates over all instance lists and prints frequency counts for the top 10 items

        """
        for k,v in {'Hashtag': self.hashtags, 'Screen Name': self.screen_names, 'Word': self.words}.items():
            pt = PrettyTable(field_names=[k, 'Count'])
            c = collections.Counter(v)
            [pt.add_row(kv) for kv in c.most_common()[1:10]]
            pt.align[k], pt.align['Count'] = 'l', 'r'
            print(pt)

##############################
# MAIN (TEST FUNCTION)       #
##############################


def main():
    with open('tweets.txt') as f:
        data = json.loads(f.read())

    t = Statistics(data)
    t.print_prettytable()


if __name__ == "__main__":
    main()
