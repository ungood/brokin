# -*- coding: utf-8 -*-
import logging, inspect
from hashlib import md5

from google.appengine.api import memcache
from google.appengine.ext import db

def serialize_entities(models):
    """Serializes either a db.Model instance or a list of them as protobufs."""
    if models is None:
        return None
    elif isinstance(models, db.Model):
        # Just one instance
        return db.model_to_protobuf(models).Encode()
    else:
        # A list
        return [db.model_to_protobuf(item).Encode() for item in models]


def deserialize_entities(data):
    """Deserializes a protobuf into either a single db.Model or a list of them."""
    if data is None:
        return None
    elif isinstance(data, str):
        # Just one instance
        return db.model_from_protobuf(data)
    else:
        return [db.model_from_protobuf(item) for item in data]


# CPAL Conde Nast - http://code.reddit.com/LICENSE
def make_key(iden, *a, **kw):
    """
    A helper function for making memcached-usable cache keys out of
    arbitrary arguments. Hashes the arguments but leaves the `iden'
    human-readable
    """
    h = md5()

    def _conv(s):
        if isinstance(s, str):
            return s
        elif isinstance(s, unicode):
            return s.encode('utf-8')
        elif isinstance(s, (tuple, list)):
            return ','.join(_conv(x) for x in s)
        elif isinstance(s, dict):
            return ','.join('%s:%s' % (_conv(k), _conv(v))
                            for (k, v) in sorted(s.iteritems()))
        else:
            return str(s)

    iden = _conv(iden)
    h.update(iden)
    h.update(_conv(a))
    h.update(_conv(kw))
    return '%s(%s)' % (iden, h.hexdigest())


def memoize(key, returns_entity=False, time=60):
    """Decorator to memoize functions using memcache.
    
    Arguments:
    key             - a unique string to use as prefix for the key.
    returns_entity  - if true, we will treat results from the wrapped function as
                      GAE entities (default: False)
    time            - the time, in seconds, to keep the results in cache (default: 60)
    """
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            cache_key = make_key(key, *args, **kwargs)
            
            data = memcache.get(cache_key)
            if data is not None:
                logging.debug("Cache Hit: %s" % cache_key)
                return deserialize_entities(data) if returns_entity else data
            
            logging.debug("Cache Miss: %s" % cache_key)
            data = fxn(*args, **kwargs)
            serialized = serialize_entities(data) if returns_entity else data
            memcache.set(cache_key, serialized, time)
            
            return data
        return wrapper
    
    return decorator