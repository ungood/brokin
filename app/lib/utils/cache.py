# -*- coding: utf-8 -*-
import logging

from google.appengine.api import memcache

def memoize(key_format, time=60):
    """Decorator to memoize functions using memcache.
    
    Arguments:
    key_format
    """
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            key = key_format % args[1:]
            
            data = memcache.get(key)
            if data is not None:
                logging.debug("Cache Hit: %s" % key)
                return data
            
            logging.debug("Cache Miss: %s" % key)
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper
    
    return decorator