from flask import Flask
from main.main import run_main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_email():
    run_main()

if __name__ == '__main__':
    app.run(debug=True)