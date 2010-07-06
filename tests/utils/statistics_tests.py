# -*- coding: utf-8 -*-
import unittest
from utils.statistics import constrain, CounterShard, Counter

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