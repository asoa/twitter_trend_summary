#!/usr/bin/env python3

from urllib.parse import unquote
import json


class TwitterQuery(object):
    """ send query to twitter api

    Attributes:
        twitter_api(authenticate.Authenticate): authenticated twitter instance
        query_type(string): type of query (i.e - trends, search)
        woeid(string): code that represents geographic location
        current_batch(int): current iteration of twitter search call
        num_batch(int): number of twitter search api calls to send
        next_query_kwargs(dict): values that tell the search api where to start the next query batch from
        query_result(json): twitter search api json result
        kwargs(dict): search api keyword arguments passed to constructor (i.e q)
        out_file(str): filename to write tweets
        json_list(list): list of tweets, 1 for each batch
        statuses(list):
    """
    WOEID = {'US': 23424977, 'WORLD': 1}

    def __init__(self, twitter_api=None, query_type=None, woeid=None, **kwargs):
        self.twitter_api = twitter_api
        self.woeid = self.WOEID.get(woeid, 23424977)
        self.query_type = query_type
        self.current_batch = 0
        self.num_batches = 5
        self.next_query_kwargs = {}
        self.query_result = None
        self.kwargs = {k: v for k, v in kwargs.items()}
        self.out_file = self.kwargs.get('out_file', False)
        self.json_list = []
        self.send_query()
        self.statuses = []

    def __repr__(self):
        string_repr = str(self.query_result)
        return string_repr

    def send_query(self):
        """ Sends n(num_batches) queries to twitter api and appends api results to file
        Args:

        Returns: None
        """
        if not self.out_file:  # don't write output to file
            try:
                if self.query_type == 'trends':
                    self.query_result = self.twitter_api.trends.place(_id=self.woeid)
                elif self.query_type == 'search':
                    self.query_result = self.twitter_api.search.tweets(q=self.kwargs.get('q'), count=self.kwargs.get('count', 100))
                    self.statuses.append(self.query_result['statuses'])
                else:
                    pass
            except Exception as e:
                print("Exception thrown: " + str(e))

        else:  # write output to file
            with open('tweets.txt', 'w') as f:
                self.query_result = self.twitter_api.search.tweets(q=self.kwargs.get('q'), count=self.kwargs.get('count', 100))
                self.json_list.append(self.query_result)
                # append results to file while get_next_batch() returns True-indicating more tweets are available
                while self.get_next_batch() and (self.current_batch < self.num_batches):
                    self.json_list.append(self.query_result)
                f.write(json.dumps(self.json_list))

    def get_scope(self, region):
        """ gets the scope of the query (i.e. us or world)

        Args:
            region (string): i.e 'US', 'WORLD'. Defaults to 'US'
        Returns: region key value
        """
        return self.WOEID.get(region)

    def get_next_batch(self):
        """ Queries search api until no more tweets for a particular status remain or batch_size is reached

        Returns: True/False (boolean) indicating if more tweets are available
        """
        try:
            if self.get_next_results_kwargs():
                self.query_result = self.twitter_api.search.tweets(**self.next_query_kwargs)
                print('Getting batch {}'.format(self.current_batch))
                self.current_batch += 1
                return True

        except Exception as e:
            print('Exception in get_next_batch(): ' + str(e))
            return False

        return False  # no next_results

    def get_next_results_kwargs(self):
        """ Gets the kwargs from the next_results value in query_result
        Returns: (boolean) True if kwargs is not None, False otherwise
        """
        try:
            # next_results: ?max_id=1089616517329809407&q=%23MothersDay&count=100&include_entities=1
            next_results = self.query_result['search_metadata']['next_results']
            self.next_query_kwargs = dict([kv.split('=') for kv in unquote(next_results[1:]).split('&')])

        except KeyError as k:
            print('No more tweets')
            return False

        except Exception as e:
            print('Exception in get_next_query_kwargs: ' + str(e))
            return False

        if len(self.next_query_kwargs) > 0:  # checks to make sure that kwargs is valid
            return True

        # return False  # no more tweets available
