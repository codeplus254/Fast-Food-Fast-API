import os
from api.v2 import init_db
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    def __init__(self):
        self.DEBUG = True
        self.TESTING = False
        self.CSRF_ENABLED = True
    

class ProductionConfig(Config):
    def __init__(self):
        self.DEBUG = False


class StagingConfig(Config):
    def __init__(self):
        DEVELOPMENT = True
        DEBUG = True


class DevelopmentConfig(Config):
    def __init__(self):
        self.database = 'fast_food_fast_db'
        self.DEVELOPMENT = True
        self.DEBUG = True
    


class TestingConfig(Config):
    def __init__(self):
        self.TESTING = True
        self.database = 'postgres'
    


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing":TestingConfig,
    "staging":StagingConfig
}