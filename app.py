from main import run_main
from lib import global_vars as globals

from quart import Quart, send_from_directory

app = Quart(__name__)

route_suffix = globals.FILENAME_DOCX.split('.')[0]
@app.route(f'/{route_suffix}', methods=['GET'])
async def get_email():
    await run_main()
    return await send_from_directory('', globals.FILENAME_DOCX, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)