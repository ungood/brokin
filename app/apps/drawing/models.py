# -*- coding: utf-8 -*-
import logging, re, base64

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from tipfy import url_for
from tipfy.ext.db import get_by_key_name_or_404

from apps.users.models import CustomUser
from utils import cache, keys

_data_url_regex = re.compile(r'^data:(?P<type>[^;]+);base64,(?P<content>.+)$')
_key_generator  = keys.KeyGenerator()

content_types  = [ 'image/png' ]

class Image(db.Model):
    full_size    = db.BlobProperty(required=True)
    thumbnail    = db.BlobProperty()
    content_type = db.StringProperty(required=True, choices=content_types)
    
    @classmethod
    def create(cls, data_url, **kwargs):
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
    
    @classmethod    
    @cache.memoize('Image-%s')
    def get_or_404(cls, key_name):
        return get_by_key_name_or_404(Image, key_name)
    

class Post(polymodel.PolyModel):
    """Base class representing either an image or a text post."""
    reply_to        = db.SelfReferenceProperty(collection_name='replies')
    
    author          = db.ReferenceProperty(collection_name='posts')
    # Caches the username of the author so we don't have to always look it up.
    author_username = db.StringProperty()
    # Store the session that created the post so that if an anonymous user
    # creates an account, his already-made posts will be tied to it.
    session_key     = db.StringProperty()    
    
    created  = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
        
    def __unicode__(self):
        return self.slug()
        
    @classmethod
    @cache.memoize('Post-%s')
    def get_or_404(cls, key_name):
        return get_by_key_name_or_404(Post, key_name)
    
    @classmethod    
    @cache.memoize('Post-recent')
    def list_recent(cls):
        return Post.all().order('-created').fetch(10)

        
class ImagePost(Post):
    image     = db.ReferenceProperty(Image, required=True)
    
    @property
    def image_key(self):
        """Gets the key_name of image without hitting the datastore."""
        return ImagePost.image.get_value_for_datastore(self).name()
    
    @classmethod
    def create(cls, image):
        key = _key_generator.create_key()
        logging.debug('Creating a new ImagePost: %s' % key)
        return ImagePost(key_name=key, image=image)
    
    
class TextPost(Post):
    text = db.StringProperty(required=True, multiline=False)
    
    @classmethod
    def create(self, text):
        key = _key_generator.create_key()
        logging.debug('Creating a new TextPost: %s' % key)
        return TextPost(key_name=key, text=text)