from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)

@app.get('/')
def index():
    return 'Hello World!'

if(__name__ == '__main__'):
    app.run(debug=True)