# -*- coding: utf-8 -*-
from google.appengine.ext import db

from apps.drawing.models import Post
from apps.users.models import CustomUser
from utils.statistics import constrain


class Vote(db.Model):
    post = db.ReferenceProperty('p', Post, required=True, collection_name='votes')
    user = db.ReferenceProperty('r', CustomUser, required=True, collection_name='votes')
    
    value = db.IntegerProperty('v', default=0)
            
    created = db.DateTimeProperty('c', auto_now_add=True)
    updated = db.DateTimeProperty('u', auto_now=True)

    @staticmethod
    def create_or_update(post, user, value):
        post_key   = post.key().name()
        user_key   = user.key().name()
        vote_key   = '%s-%s' % (post_key, user_key)
    
        old_value  = 0
        def txn:
            vote = Vote.get_by_key_name(key_name)
            if not vote:
                vote = Vote(key_name=key_name, post=post, user=user)
            old_value = vote.value
            vote.put()
        db.run_in_transaction(txn)
        
        upvotes   = constrain(value - old_value, -1, 1)
        downvotes = constrain(old_value - value, -1, 1)
        
        post.upvotes += upvotes
        post.downvotes += downvotes
        if post.author:
            post.author.karma += (upvotes - downvotes)
