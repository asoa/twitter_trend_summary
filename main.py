#!/usr/bin/env python3

import authenticate
import query
import statistics


def prompt(top_trends):
    """Prompt user to enter integer selection for hashtag to get statistics for
    Args:
        top_trends: (list) sorted list on tweet volume
    Returns: None

    """
    print("The top trends sorted by count are: \n")
    for n in range(0, 10):
        print("\t{}: {} {}".format(n + 1, top_trends[n][0], top_trends[n][1]))


def main():
    api = authenticate.Authenticate()
    q = query.TwitterQuery(twitter_api=api.twitter_api, query_type='trends')

    top_trends = sorted([(trend['name'], trend['tweet_volume']) for trend in q.query_result[0]['trends']
                            if trend['tweet_volume'] is not None],
                            key=lambda x: x[1], reverse=True)

    hashtag = 0
    while hashtag not in range(1, 11):  # loop while hashtag isn't in range
        try:
            prompt(top_trends)
            hashtag = int(input("\nWhat hashtag to you want to get statistics for? "))

            assert hashtag in range(1, 11)  # if hashtag isn't in range, throw exception

            tweets = query.TwitterQuery(api.twitter_api, query_type='search', q=top_trends[hashtag-1][0], out_file=True)
            stats = statistics.Statistics(tweets.json_list)
            stats.print_prettytable()

            hashtag = 0  # resets hashtag back to 0 to continue to prompt user for hashtag selection
        except:
            print(" ***** Choose hashtag between 1 and 10 ***** \n")
            # prompt(top_trends)


if __name__ == "__main__":
    main()
