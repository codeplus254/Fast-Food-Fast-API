import sys
#sys.path.insert(0,'/home/andela/Fast-Food-Fast-API')
from api import create_app
import os
from os.path import join, dirname
#from dotenv import load_dotenv

# Create .env file path.
#dotenv_path = join(dirname(__file__), '.env')
dotenv_path = join(os.path.dirname(os.path.realpath(__file__)),'.env')

# Load file from the path.

#load_dotenv(dotenv_path=dotenv_path)
config_name = os.getenv("APP_SETTINGS")
APP = create_app(config_name)

if __name__ == '__main__':
    
    APP.run(debug=True)

