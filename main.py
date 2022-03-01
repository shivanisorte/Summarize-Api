from flask import Flask

app = Flask(__name__)

@app.get('/')
def index():
    return { 'message':"hello"}

@app.get('/shivani')
def get_name(name: str):
    return { 'hello ': f'{name}'}

if __name__ == '__main__':
    app.run(port=3333)