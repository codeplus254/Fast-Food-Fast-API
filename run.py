import sys
#sys.path.insert(0,'/home/andela/Fast-Food-Fast-API')
from api import create_app
import os

config_name = os.getenv("APP_SETTINGS")
#print(configuration_key)
APP = create_app(config_name)

if __name__ == '__main__':
    
    APP.run(debug=True)

