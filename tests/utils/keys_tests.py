# -*- coding: utf-8 -*-
import unittest

from utils import keys

class KeysTest(unittest.TestCase):
    def base62_encode_test(self):
        self.assertEqual('0'   , keys.baseX_encode(0))
        self.assertEqual('lz'  , keys.baseX_encode(1337))
        self.assertEqual('00lz', keys.baseX_encode(1337, chars=4))
        
    def base62_decode_test(self):
        self.assertEqual(0,    keys.baseX_decode('0'))
        self.assertEqual(1337, keys.baseX_decode('lz'))
        self.assertEqual(1337, keys.baseX_decode('00lz'))
        
    def create_key_test(self):
        kg11 = keys.KeyGenerator(11)
        kg6  = keys.KeyGenerator(6)
        
        self.assertEqual(11, len(kg11.create_key()))
        self.assertEqual(6,  len(kg6.create_key()))