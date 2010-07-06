# -*- coding: utf-8 -*-
import unittest

class MetaTests(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)
        
    def test_equals(self):
        self.assertEquals(1, 1)