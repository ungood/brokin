# -*- coding: utf-8 -*-
import logging, tipfy
from google.appengine.ext import db

from utils.handlers import BaseHandler
from apps.users.models import CustomUser
from models import Image, Post, ImagePost, TextPost


class ViewImageHandler(BaseHandler):
    def get(self, image_key):
        image = Image.get_or_404(image_key)
        return tipfy.Response(image.full_size, mimetype=image.content_type)


class BasePostHandler(BaseHandler):
    def dispatch(self, *args, **kwargs):
        self.context = self.context or {}
                
        return RequestHandler.dispatch(self, *args, **kwargs)
    
    def _assign_user(self, post):
        session_key      = None if self.session == None else self.session.get('key')
        post.author      = CustomUser.get_current_user()
        post.session_key = session_key
    
    def _create_image_post(self):
        """Creates a new ImagePost from the form variables."""
        data = tipfy.request.form.get('post-image')
        image = Image.create(data)
        post = ImagePost.create(image)
        self._assign_user(post)
        image.put()
        return post
    
    def _create_text_post(self):
        """Creates a new TextPost from the form variables."""
        text = tipfy.request.form.get('post-text')
        post = TextPost.create(text)
        self._assign_user(post)
        return post    


class ViewPostHandler(BasePostHandler):
    def get(self, post_key):
        """GETs a page that displays a single post, and its replies."""
        post = Post.get_or_404(post_key)
        if isinstance(post, ImagePost):
            return self._get_image(post)
        else:
            return self._get_text(post)
    
    def _get_image(self, post):
        return self.render_response('drawing/view-post-image.html', post=post)
    
    def _get_text(self, post):
        return self.render_response('drawing/view-post-text.html', post=post)
    
    def post(self, post_key):
        parent = Post.get_or_404(post_key)
        new_post = None
        if isinstance(parent, ImagePost):
            new_post = self._create_text_post()
        else:
            new_post = self._create_image_post()
        parent.add_reply(new_post)
        new_post.put()
        return tipfy.redirect_to('view-post', post_key=new_post.key().name())


class NewPostHandler(BasePostHandler):
    def get(self):
        """Returns a page that displays the drawing form."""
        return self.render_response('drawing/new-post.html')
    
    def post(self):
        """Save a new post and redirect the user to a random one."""
        post = self._create_image_post()
        post.put()
                
        return tipfy.redirect_to('view-post', post_key=post.key().name())