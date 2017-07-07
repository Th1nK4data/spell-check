import os

import falcon

import constants
from correction import controller


def get_config():
    """
        get config from envorinment variables -> dict
    """
    ret = {
        constants.CFG_MOVIES_PINYIN_DICT_PATH: os.environ.get(
            constants.ENV_MOVIES_PINYIN_DICT_PATH,
            constants.DFL_MOVIE_PINYIN_DICT_PATH)
    }

    return ret

# get server config
config = get_config()
# get map of news API handlers
handler_map = controller.get_handler_map(config)
# init API server from falcon
# init API server from falcon
api = falcon.API()
for endpoint, handler in handler_map.items():
    # add route from endpoint to handler
    api.add_route(endpoint, handler)
