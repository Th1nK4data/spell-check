import logging
import json
from collections import defaultdict

import falcon

from cache import DictCache
from .service import CorrectionService
from .common import time_calc_decorator


def get_handler_map(config):
    """
    """
    correctionHandler = CorrectionV1Handler(config)
    healthCheckHandler = HealthCheckHandler(config)
    return {
        '/correction/v1/{text}': correctionHandler,
        '/correction/_health_check': healthCheckHandler
    }


def setup_route(config, api):
    '''route function to handle restful api

    /correction/v1/<text>
    '''
    CorrectionV1Handler.config = config
    CorrectionV1Handler.service = CorrectionService(config)
    CorrectionV1Handler.cache = DictCache()

    api.add_resource(CorrectionV1Handler, '/correction/v1')
    # api.add_resource(HealthCheckHandler, '/_health_check')


class HealthCheckHandler(object):
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.service = CorrectionService(config)
        super(HealthCheckHandler, self).__init__()

    def on_get(self, req, rsp):
        self.logger.info('_health_check!')
        resp = self.service.correction(u'给我徐子摩')
        if resp['spellCheck'] == u'给我徐志摩':
            rsp.body = u'ok'
        else:
            rsp.body = resp['stateCode']
        self.logger.info('_health_check done. %s', rsp.body)
        rsp.status = falcon.HTTP_200


class CorrectionV1Handler(object):
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.service = CorrectionService(config)
        self.cache = DictCache()
        super(CorrectionV1Handler, self).__init__()

    def on_get(self, req, rsp, text):
        rsp_content = self.cache.get(text)
        if rsp_content:
            self.logger.info('cache hit(%s)', text)
        else:
            self.logger.info('cache miss(%s)', text)
            rsp_content = self.service.correction(text)
            # TODO(mike): handle rsp_failed case
            self.cache.update(text, rsp_content)

        rsp.body = json.dumps(rsp_content)
        self.logger.info('%s', rsp_content)
        rsp.status = falcon.HTTP_200
