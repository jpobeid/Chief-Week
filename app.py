from main import run_main

from quart import Quart, send_from_directory

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def get_email():
    await run_main()
    return await send_from_directory('', 'weekly_email.docx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)