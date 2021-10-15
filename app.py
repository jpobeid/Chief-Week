from flask import Flask, send_from_directory
from main import run_main
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

app = Flask(__name__)

@app.route('/', methods=['GET'])
async def get_email():
    await run_main()
    return send_from_directory('', 'weekly_email.docx', as_attachment=True)

if __name__ == '__main__':
    asgi_app = WsgiToAsgi(app)
    asyncio.run(serve(asgi_app, Config()))