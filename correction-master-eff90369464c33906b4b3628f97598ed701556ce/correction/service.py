# -*- coding: utf-8 -*-
import logging
import pickle

import pinyin

import constants
#from .common import time_calc_decorator
from common import time_calc_decorator


def getpinyin(s):
    return pinyin.get(s, format='strip', delimiter=' ')


def getFuzzyPinyin(pin):
    fuzzy = set([pin])
    # 处理方言
    fangyan = [['n', 'l', 'r'], ['f', 'h'], ['q', 'c'], ['r', 'y']]
    for fy in fangyan:
        if pin[0] in fy:
            fuzzy.update(set([i + pin[1:] for i in fy]))
    # 处理平翘舌
    pingshe = ['z', 'c', 's']
    if pin[0] in pingshe and pin[1] == 'h':
        fuzzy.update(set([pin, pin[0] + pin[2:]]))
    elif pin[0] in pingshe and pin[1] != 'h':
        fuzzy.update(set([pin, pin[0] + 'h' + pin[1:]]))
    # 处理前后鼻音
    fuzzy2 = list(fuzzy)
    for cand in fuzzy:
        if cand[-1] == 'g':
            fuzzy2.append(cand[:-1])
        elif cand[-1] == 'n':
            fuzzy2.append(cand + 'g')
    return list(set(fuzzy2))  # fuzzy可能包含非法拼音，例如rian, riang


def same(p1, p2):
    return p2 in getFuzzyPinyin(p1)


def match(part, movie):
    for l in range(len(part)):
        if not same(part[l], movie[l]):
            return False
    return True


class CorrectionService(object):
    def __init__(self, config):
        super(CorrectionService, self).__init__()
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._load_movies()

    def _load_movies(self):
        path = self.config[constants.CFG_MOVIES_PINYIN_DICT_PATH]
        try:
            with open(path, 'rb') as f:
                self.movies = pickle.load(f)
        except Exception as exp:
            raise exp

    def correction(self, s):
        self.logger.debug('s: %s', s)
        ret_s = s
        err = None
        try:
            ps = getpinyin(s).split(' ')
            sl = len(s)
            maxlen = min(sl, max(self.movies))
            for l in range(maxlen, 0, -1):
                for i in range(sl-l, -1, -1):
                    ppart = ps[i:i+l]
                    if l in self.movies:
                        for pmovie in self.movies[l]:
                            movie = self.movies[l][pmovie]
                            pmovie = pmovie.split(' ')
                            if match(ppart, pmovie):
                                ret_s = s[:i] + movie + s[i+l:]
        except Exception as exp:
            self.logger.exception('')
            err = exp
        finally:
            return {
                "query": s,
                "spellCheck": ret_s,
                "madeChange": ret_s != s,
                "stateCode": 0 if err is None else -1
            }


if __name__ == '__main__':
    # python -m correction.service
    import os

    path = os.path.dirname(__file__)
    config = {
        constants.CFG_MOVIES_PINYIN_DICT_PATH: os.path.join(
            path, 'movies_pin_name_dict.pkl')
    }
    print (config)
    obj_ = CorrectionService(config)
    ret = obj_.correction('给我播放徐子墨')
    print (ret)
    ret = obj_.correction('我想看半月传')
    print (ret)
