from flask import Flask
from main import run_main
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

app = Flask(__name__)

@app.route('/', methods=['GET'])
async def get_email():
    await run_main()
    return 'All done!!!'

if __name__ == '__main__':
    asgi_app = WsgiToAsgi(app)
    asyncio.run(serve(asgi_app, Config()))