import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
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
    #print(os.getenv('DATABASENAME'))
    #os.environ.pop("DATABASENAME")
    #print(os.getenv('DATABASENAME'))
    #os.environ['DATABASENAME'] = 'test_fast_food_fast'
    #print(os.getenv('DATABASENAME'))
app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing":TestingConfig,
    "staging":StagingConfig
}