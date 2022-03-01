from time import time
from flask import Flask
import json, time

#create flask server
app = Flask(__name__)

#handle paths
@app.route('/', methods=['GET'])
def home_page():
    data_set = {'Message':'Data from API', 'Timestamp':time.time()}
    json_dump = json.dumps(data_set)

    return json_dump  

if __name__ =="__main__":
    app.run(port=3333)
