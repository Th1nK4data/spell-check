# -*- coding: utf-8 -*-
import time
from collections import OrderedDict


class DictCache(object):
    def __init__(self, expiration=30*60, entry=1000):
        self.expiration = expiration
        self.cache = OrderedDict()
        self.entry = entry

    def get(self, k):
        v = self.cache.get(k)
        if v and time.time() < v['expiration']:
            return v['data']
        return None

    def update(self, k, v):
        v_ = {
            'data': v,
            'expiration': time.time() + self.expiration
        }

        if len(self.cache.keys()) >= self.entry:
            # pop first insert item
            try:
                self.cache.popitem(last=False)
            except:
                pass
        self.cache[k] = v_


if __name__ == '__main__':
    cache = DictCache(expiration=5)
    cache.update('a', 5)
    print (cache.get('a'))
    time.sleep(5)
    print (cache.get('a'))
