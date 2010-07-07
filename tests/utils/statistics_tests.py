# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, timedelta
from utils.statistics import *

class StatisticsTest(unittest.TestCase):
    def constrain_test(self):
        self.assertEqual(12,  constrain(12, 0, 100))
        self.assertEqual(0,   constrain(-1, 0, 100))
        self.assertEqual(100, constrain(1010, 0, 100))
    
    def CounterShard_test(self):
        count1 = CounterShard.get_count('test', 'key1')
        self.assertEqual(0, count1)
        
        CounterShard.add('test', 'key1', 15)
        count1 = CounterShard.get_count('test', 'key1')
        self.assertEqual(15, count1)
        
        count2 = CounterShard.get_count('test', 'key2')
        self.assertEqual(0, count2)
        
        CounterShard.add('test', 'key2', -1)
        count2 = CounterShard.get_count('test', 'key2')
        self.assertEqual(-1, count2)
        
        count1 = CounterShard.get_count('test', 'key1')
        self.assertEqual(15, count1)
        
    def Counter_test(self):
        c1 = Counter('foobar', 'foo')
        c2 = Counter('foobar', 'bar')
        self.assertEqual(0, int(c1))
        self.assertEqual(0, int(c2))
        
        c1 += 10
        c2 -= -15
        self.assertEqual(10, int(c1))
        self.assertEqual(15, int(c2))
        
        c2 -= 10
        self.assertEqual(10, int(c1))
        self.assertEqual(5, int(c2))
        
        # Counter shouldn't have a minimum of 0?
        c2 -= 10
        self.assertEqual(-5, int(c2))
        
class ScoreTests(unittest.TestCase):
    def top_score_test(self):
        self.assertEqual(0, top_score(0, 0))
        self.assertEqual(10, top_score(20, 10))
        self.assertEqual(-1, top_score(3, 4))
        
    def wilson_score_test(self):
        self.assertEqual(0      , wilson_score(0, 0))
        self.assertEqual(5000000, wilson_score(1, 1))
        self.assertEqual(7748633, wilson_score(7, 3))
        self.assertEqual(9967642, wilson_score(1000, 5))
        
    def hot_and_lonely_test(self):
        today    = datetime.today()
        tomorrow = today + timedelta(days=1)
        
        (h1, l1) = hot_and_lonely(100, 0, 0, today)
        (h2, l2) = hot_and_lonely(10, 0, 0, tomorrow)
        (h3, l3) = hot_and_lonely(100, 0, 5, today)
        
        # A post with 10x votes should have the same score as one 24 hours in the future.
        self.assertEqual(h1, h2)
        
        # A post with 5 replies should have a lower lonely score.
        self.assertTrue(l3 < l1)
        self.assertTrue(l3 < l2)