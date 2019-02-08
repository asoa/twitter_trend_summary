#!/usr/bin/env python3

import authenticate
import query
import statistics


TREND_LENGTH = 0


def prompt(top_trends):
    """Prompt user to enter integer selection for hashtag to get statistics for
    Args:
        top_trends: (list) sorted list on tweet volume
    Returns: None

    """
    print("The top trends sorted by count are: \n")
    for n in range(0, TREND_LENGTH):
        print("\t{}: {} {}".format(n + 1, top_trends[n][0], top_trends[n][1]))


def main():
    global TREND_LENGTH
    api = authenticate.Authenticate()
    q = query.TwitterQuery(twitter_api=api.twitter_api, query_type='trends')

    top_trends = sorted([(trend['name'], trend['tweet_volume']) for trend in q.query_result[0]['trends']
                            if trend['tweet_volume'] is not None],
                            key=lambda x: x[1], reverse=True)

    TREND_LENGTH = len(top_trends)

    hashtag = 0
    while hashtag not in range(1, TREND_LENGTH):  # loop while hashtag isn't in range
        try:
            prompt(top_trends)
            hashtag = int(input("\nWhat hashtag do you want to get statistics for? "))

            assert hashtag in range(1, TREND_LENGTH + 1)  # if hashtag isn't in range, throw exception

            tweets = query.TwitterQuery(api.twitter_api, query_type='search', q=top_trends[hashtag-1][0], out_file=True)
            stats = statistics.Statistics(tweets.json_list)
            stats.print_prettytable()

            hashtag = 0  # resets hashtag back to 0 to continue to prompt user for hashtag selection
        except:
            print(" ***** Choose hashtag between 1 and {} ***** \n".format(TREND_LENGTH))
            # prompt(top_trends)


if __name__ == "__main__":
    main()
