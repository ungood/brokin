# -*- coding: utf-8 -*-
import logging, re, base64

from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from tipfy import url_for
from tipfy.ext.db import get_by_key_name_or_404

from apps.users.models import CustomUser
from utils.cache import memoize, CachedQueue
from utils import keys, statistics

_data_url_regex = re.compile(r'^data:(?P<type>[^;]+);base64,(?P<content>.+)$')
_key_generator  = keys.KeyGenerator()

content_types  = [ 'image/png' ]

class Image(db.Model):
    full_size    = db.BlobProperty('f', required=True)
    thumbnail    = db.BlobProperty('t')
    content_type = db.StringProperty('c', required=True, choices=content_types)
    
    @staticmethod
    def create(data_url, **kwargs):
        """Creates a new Image from an uploaded file in Data-URL format."""
        key = _key_generator.create_key()
        logging.debug('Creating a new Image: %s' % key)
        
        match = _data_url_regex.match(data_url)
                
        content_type = match.group('type')
        b64encoded = match.group('content')
        full_size = base64.b64decode(b64encoded)
        # todo: more error checking
        # todo: set off a task to create the thumbnail.
        return Image(key_name     = key,
                     content_type = content_type,
                     full_size    = full_size)
    
    @staticmethod    
    @memoize('Image.get', is_entity=True)
    def get_or_404(key_name):
        return get_by_key_name_or_404(Image, key_name)
    

class Post(polymodel.PolyModel, statistics.StatisticsMixin):
    """Base class representing either an image or a text post."""
    reply_to        = db.SelfReferenceProperty('r', collection_name='replies')
    
    author          = db.ReferenceProperty('a', collection_name='posts')
    # Store the session that created the post so that if an anonymous user
    # creates an account, his already-made posts will be tied to it.
    session_key     = db.StringProperty('s')    
    
    created = db.DateTimeProperty('c', auto_now_add=True)
    updated = db.DateTimeProperty('u', auto_now=True)
    
    @property
    def key_name(self):
        return self.key().name()
    
    @property
    def author_key(self):
        return Post.author.get_value_for_datastore(self).name()
    
    @property
    def author_username(self):
        return author.username if author else None
    
    @property
    def upvote_counter(self):
        return statistics.Counter('upvotes', self.key_name)
        
    @property
    def reply_counter(self):
        return statistics.Counter('downvotes', self.key_name)
        
    @property
    def reply_counter(self):
        return statistics.Counter('replies', self.key_name)
    
    def update_scores(self):
        self.upvotes     = int(self.upvote_counter)
        self.downvotes   = int(self.downvote_counter)
        self.reply_count = int(self.reply_counter)
        
        return statistics.StatisticsMixin(self, self.created)
    
    def add_reply(self, reply):
        reply.reply_to = self
        self.reply_counter += 1
        self.create_update_task()
        
    def create_update_task(self):
        queue = CachedQueue('update_post')
        task = taskqueue.Task(countdown=30, params = {
            'post_key' : self.key_name  
        })
        queue.add(self.key_name, task)
    
    @staticmethod
    @memoize('Post.get', is_entity=True)
    def get_or_404(key_name):
        return get_by_key_name_or_404(Post, key_name)
    
    @staticmethod    
    @memoize('Post.recent', is_entity=True)
    def list_recent():
        return Post.all().order('-created').fetch(10)

        
class ImagePost(Post):
    image     = db.ReferenceProperty('i', Image, required=True)
    
    @property
    def image_key(self):
        """Gets the key_name of image without hitting the datastore."""
        return ImagePost.image.get_value_for_datastore(self).name()
    
    @staticmethod
    def create(image):
        key = _key_generator.create_key()
        logging.debug('Creating a new ImagePost: %s' % key)
        return ImagePost(key_name=key, image=image)
    
    
class TextPost(Post):
    text = db.StringProperty('t', required=True, multiline=False)
    
    @staticmethod
    def create(text):
        key = _key_generator.create_key()
        logging.debug('Creating a new TextPost: %s' % key)
        return TextPost(key_name=key, text=text)