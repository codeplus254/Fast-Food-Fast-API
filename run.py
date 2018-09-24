import sys
sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from api.v1.api_v1 import APP

if __name__ == '__main__':
    APP.run(debug=False)

