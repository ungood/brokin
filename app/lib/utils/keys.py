# -*- coding: utf-8 -*-
import random, base64

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def baseX_encode(num, chars=1, alphabet=BASE62_ALPHABET):
    """Encode a number in Base X
    
    See: http://stackoverflow.com/questions/1119722/base-62-conversion-in-python/1119769#1119769

    Arguments:
    num      -- The number to encode
    chars    -- The minimum number of chars to encode (default 1)
    alphabet -- The alphabet to use for encoding (default base62)
    >>> baseX_encode(0)
    '0'
    """
    arr = []
    base = len(alphabet)
    while chars > 0:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
        chars -= 1
        
    arr.reverse()
    return ''.join(arr)
        

def baseX_decode(string, alphabet=BASE62_ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    string   -- The encoded string
    alphabet -- The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

class KeyGenerator():
    def __init__(self, length=11):
        self.length = length
    
    def create_key(self):
        """Creates a unique string key that can be used as key_name.
    
        Operates similarly to youtube's algorithm: Generate a bunch of bits of
        randomness and then base62 encode for a (hopefully) unique key.
        """
        bits = 6 * self.length # ln(62) == 6
        num = random.getrandbits(bits)
        return baseX_encode(random.getrandbits(bits), chars=self.length)
