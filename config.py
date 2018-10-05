import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'andela'
    HOSTNAME='localhost'
    PASSWORD='Milionea1'
    SALT='fast-food-fast'
    ADMIN_NAME='admin'
    ADMIN_PASSWORD='postgres'
    os.environ['DATABASENAME']= 'fast_food_fast_db'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    os.environ.pop("DATABASENAME")
    os.environ['DATABASENAME'] = 'test_fast_food_fast'
app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing":TestingConfig,
    "staging":StagingConfig
}