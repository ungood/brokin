# -*- coding: utf-8 -*-
import random
import logging
from math import sqrt, log
from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache

import tipfy
import pytz

from utils.cache import memoize, make_key

def constrain(amt, low, high):
    """Constrains a value between low and high."""
    if amt < low:
        return low
    elif amt > high:
        return high
    else:
        return amt


class CounterShardConfig(db.Model):
    """Tracks the number of shards for each named counter."""
    name        = db.StringProperty(required=True)
    num_shards  = db.IntegerProperty(required=True, default=5)
    
    @staticmethod
    @memoize('get_num_shards')
    def get_num_shards(name):
        config = CounterShardConfig.get_or_insert(name, name=name)
        return config.num_shards
    
    @staticmethod
    def increase_shards(name, num):
        """Increase the number of shards for a given sharded counter.
        Will never decrease the number of shards.
    
        Arguments:
          name - The name of the counter
          num  - How many shards to use
        """
        config = CounterShardConfig.get_or_insert(name, name=name)
        def txn():
            if config.num_shards < num:
                config.num_shards = num
                config.put()
        db.run_in_transaction(txn)


class CounterShard(db.Model):
    """Tracks a counter variable of a given name for a given reference object."""
    name            = db.StringProperty(required=True)
    reference_key   = db.StringProperty('ref')
    count           = db.IntegerProperty(required=True, default=0)
    
    @staticmethod
    @memoize('counter')
    def get_count(name, key):
        """ Gets the current value of a given shard counter.
        
        Arguments:
            name  - The name of the counter
            key   - The key of the referenced object
        """
        total = 0
        query = CounterShard.all().filter('name = ', name).filter('reference_key = ', key)
        for counter in query:
            total += counter.count
        
        return total

    @staticmethod
    def add(name, key, delta):
        """Increment (or decrement) the value for a given shard counter.
        
        Parameters:
            name  - The name of the counter
            key   - The key of the referenced object
            delta - The amount to change the counter by
        """
        num_shards = CounterShardConfig.get_num_shards(name)
        def txn():
            index = random.randint(0, num_shards - 1)
            shard_key = '%s-%s-%s' % (name, key, str(index))
            counter = CounterShard.get_by_key_name(shard_key)
            if counter is None:
                counter = CounterShard(key_name=shard_key, name=name, reference_key=key)
            counter.count += delta
            counter.put()
        db.run_in_transaction(txn)
        
        cache_key = make_key('counter', name, key)
        cached = memcache.get(cache_key)
        if cached != None:
            memcache.set(cache_key, cached + delta)


class Counter:
    """A wrapper around CounterShard that gives it some convenient syntax sugar."""
    def __init__(self, name, key):
        self.name = name
        self.key  = key
    
    def __iadd__(self, other):
        CounterShard.add(self.name, self.key, other)
        return self
    
    def __isub__(self, other):
        CounterShard.add(self.name, self.key, other * -1)
        return self
        
    def __int__(self):
        return CounterShard.get_count(self.name, self.key)
        

def top_score(upvotes, downvotes):
    return upvotes - downvotes


#from CPAL-licensed code in code.reddit.com
def _wilson_score(upvotes, downvotes):
    n = float(upvotes + downvotes)
    if n == 0:
        return 0
    
    z = 1.0 # pnormaldist(confidence)
    phat = float(upvotes) / n
    result = sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    return int(result * 10e6)

_uprange     = 500
_downrange   = 100
_wilson_cache = [[_wilson_score(up, down) for down in xrange(0, _downrange)] for up in xrange(0, _uprange)]

def wilson_score(upvotes, downvotes):
    """Calculates the lower bound of Wilson score confidence interval for a
    Bernoulli parameter.
    
    http://blog.linkibol.com/2010/05/07/how-to-build-a-popularity-algorithm-you-can-be-proud-of/
    http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    """
    if 0 <= upvotes <= _uprange and 0 <= downvotes <= _downrange:
        return _wilson_cache[upvotes][downvotes]
    return _wilson_score(upvotes, downvotes)


def _lonely_coefficient(replies):
    """An easing function that maps [0, positive infinity) to [1, 0)"""
    return 1/((replies+1)**0.3)

_lonely_cache = [_lonely_coefficient(x) for x in xrange(0, 100)]

def lonely_coefficient(replies):
    return _lonely_cache[replies] if replies <= 100 else _lonely_coefficient(replies)

def hot_and_lonely(upvotes, downvotes, replies, date):
    """Calculates hotness and lonely ratings for an item, returned as a tuple.
    
    hot    - A popularity rating biased towards newer items.
    lonely - Biases the hotness rating towards items with fewer replies.
    
    Inspired from reddit.com's hotness rating - CPAL-license: code.reddit.com
    """
    score  = upvotes - downvotes
    order = log(max(abs(score), 1), 10)
    sign = 1 if score > 0 else -1 if score < 0 else 0
    hot_hours = sign * order * 24
    
    replies = max(replies, 0)
        
    hot    = timedelta(hours=hot_hours)
    lonely = timedelta(hours=hot_hours * lonely_coefficient(replies))
    return (date + hot, date + lonely)
        

class StatisticsMixin():
    """A common mixin for classes that want to implement statistics."""
    upvotes      = db.IntegerProperty('up', default=0)
    downvotes    = db.IntegerProperty('dn', default=0)
    reply_count  = db.IntegerProperty('rc', default=0)
    
    top_score    = db.IntegerProperty('ts', default=0)
    best_score   = db.IntegerProperty('bs', default=0)
    hot_score    = db.DateTimeProperty('hs')
    lonely_score = db.DateTimeProperty('ls')
    
    def update_scores(self, created):
        top_score = statistics.top_score(upvotes, downvotes)
        best_score = statistics.wilson_score(upvotes, downvotes)
        (hot_score, lonely_score) = statistics.hot_and_lonely(upvotes,
                                                              downvotes,
                                                              reply_count,
                                                              created)
        