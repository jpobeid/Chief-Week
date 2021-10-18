import os
import json

from main import run_main
from lib import global_vars as globals
from quart import Quart, send_from_directory, request, Response

app = Quart(__name__)

route_suffix = globals.FILENAME_DOCX.split('.')[0]
@app.route(f'/{route_suffix}', methods=['GET'])
async def get_email():
    await run_main()
    return await send_from_directory('', globals.FILENAME_DOCX, as_attachment=True)

@app.route('/settings', methods=['POST'])
async def set_settings():
    settings_data = await request.get_data()
    settings_json = json.loads(settings_data)
    with open(os.path.join(globals.PATH_ASSETS, globals.FILENAME_SETTINGS), 'wb') as f:
        f.write(bytes(settings_json.get(globals.KEY_SETTINGS)))
    return Response({}, status=200)

@app.route('/schedule', methods=['POST'])
async def set_schedule():
    schedule_data = await request.get_data()
    schedule_json = json.loads(schedule_data)
    with open(os.path.join(globals.PATH_ASSETS, globals.FILENAME_SCHEDULE), 'wb') as f:
        f.write(bytes(schedule_json.get(globals.KEY_SCHEDULE)))
    return Response({}, status=200)

if __name__ == '__main__':
    app.run(debug=False)