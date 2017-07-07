# -*- coding: utf-8
import os

import pytest

import constants
from correction.service import CorrectionService


service = None


@pytest.fixture(scope='session')
def movie_pinyin_path():
    dir_ = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(dir_), 'correction', 'movies_pin_name_dict.pkl')
    return path


@pytest.fixture(scope='session')
def config(movie_pinyin_path):
    return {
        constants.CFG_MOVIES_PINYIN_DICT_PATH: movie_pinyin_path
    }


@pytest.fixture(scope='session', autouse=True)
def init_service(config):
    global service
    if service is None:
        service = CorrectionService(config)
    return service


@pytest.fixture(scope='session')
def normal_case():
    return [
        {
            'text': u'给我徐子摩',
            'answer': u'给我徐志摩'
        },
        {
            'text': u'我想看半月传',
            'answer': u'我想看芈月传'
        }
    ]


def test_normal(normal_case):
    for c in normal_case:
        ret = service.correction(c['text'])
        assert ret['stateCode'] == 0, c
        assert ret['madeChange'] is True, c
        assert ret['spellCheck'] == c['answer'], c
