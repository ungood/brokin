# -*- coding: utf-8 -*-
import unittest, random
from utils.cache import memoize
from google.appengine.ext import db

j = 0

class DummyEntity(db.Model):
    foo = db.IntegerProperty()

@memoize('simple_func(%s)')
def simple_func(foo):
    global j
    
    result = foo + j
    j += 1
    return result

class DummyClass():
    def __init__(self, i):
        self.i = i
        
    @memoize('simple_method')
    def simple_method(self, foo):
        result = foo + self.i
        self.i += 1
        return result
    
    @staticmethod
    @memoize('static_method')
    def static_method(foo):
        global j
        
        result = foo + j
        j += 1
        return result

@memoize('entity_method', returns_entity=True)
def entity_method():
    global j
    j += 1
    return DummyEntity(foo=j)

class CacheTest(unittest.TestCase):
    def setUp(self):
        global j
        
        j = 0
    
    def function_test(self):
        self.assertEqual(0, simple_func(0))
        self.assertEqual(0, simple_func(0), 'Cached function result was recalculated.')
    
    def method_test(self):
        test1 = DummyClass(1)
        test2 = DummyClass(2)
        
        self.assertEqual(1, test1.simple_method(0))
        self.assertEqual(1, test1.simple_method(0), 'Cached method result was recalculated.')
        
        self.assertEqual(2, test2.simple_method(0), 'Result from another instance returned.')
        self.assertEqual(2, test2.simple_method(0), 'Cached method result was recalculated.')
        
    def static_method_test(self):
        self.assertEqual(0, DummyClass.static_method(0))
        self.assertEqual(0, DummyClass.static_method(0), 'Cached function result was recalculated.')
    
    def entity_test(self):
        dummy = entity_method()
        self.assertEqual(dummy.foo, entity_method().foo)