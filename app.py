import os
import json

from main import run_main
from lib import global_vars as globals
from lib import functions as funcs
from quart import Quart, send_from_directory, request, Response

app = Quart(__name__)

route_suffix = globals.FILENAME_DOCX.split('.')[0]
@app.route(f'/{route_suffix}', methods=['GET'])
async def get_email():
    await run_main()
    return await send_from_directory('', globals.FILENAME_DOCX, as_attachment=True)

@app.route('/settings', methods=['GET', 'POST'])
async def access_settings():
    if request.method == 'GET':
        settings = funcs.make_settings_dict()
        return Response(json.dumps(settings), status=200)
    else:
        settings_data = await request.get_data()
        settings_json = json.loads(settings_data)
        with open(os.path.join(globals.PATH_ASSETS, globals.FILENAME_SETTINGS), 'w') as f:
            for e in settings_json:
                f.write(e + globals.SETTINGS_SEPARATOR + settings_json.get(e) + '\n')
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