import os
import datetime
import numpy as np
from requests_html import AsyncHTMLSession

from . import global_vars as globals

def screen_assets():
    has_assets = os.path.exists(globals.PATH_ASSETS)
    if has_assets:
        has_settings = globals.FILENAME_SETTINGS in os.listdir(globals.PATH_ASSETS)
        has_schedule = globals.FILENAME_SCHEDULE in os.listdir(globals.PATH_ASSETS)
        return has_settings and has_schedule
    else:
        return False

def get_nearest_sunday(date):
    weekday = date.weekday()
    if weekday == 6:
        return date
    elif weekday <= 2:
        return date - datetime.timedelta(weekday + 1)
    else:
        return date + datetime.timedelta(6 - weekday)

def get_next_week():
    day = get_nearest_sunday(datetime.date.today())
    dt = 7 - day.weekday()
    return day + np.array(list(map(lambda x: datetime.timedelta(int(x)), dt + np.arange(7))))

def make_settings_dict():
    with open(os.path.join(globals.PATH_ASSETS, globals.FILENAME_SETTINGS), 'r') as f:
        settings = f.readlines()
    settings = list(map(lambda x: x.replace('\n',''), settings))
    pre_settings_dict = list(map(lambda x: x.split(globals.SETTINGS_SEPARATOR), settings))
    return dict(pre_settings_dict)

async def get_seminar_text(url_seminar, date_seminar, time_seminar):
    print('Accessing medicine lectures page...')
    sesh = AsyncHTMLSession()
    response = await sesh.get(url_seminar)
    await sesh.close()
    print('Finished accessing page!')
    month_formatted = date_seminar.strftime('%b')
    day_formatted = date_seminar.strftime('%d')
    if day_formatted.startswith('0'):
        day_formatted = day_formatted[1:]
    datetime_formatted = month_formatted + ' ' + day_formatted + ' @ ' + time_seminar
    if response.html.find('.ai1ec-event-time')[0].text.find(datetime_formatted) != -1:
        return response.html.find('.ai1ec-event-description')[0].text.replace('\xa0','')
    else:
        return '***'

def add_lecture_runs(paragraph, lecture, new_line=True):
    if lecture['Event'] == 'Holiday':
        paragraph.add_run(lecture['Event'] + ' - ' + lecture['Title'])
    elif lecture['Event'] in ['Study', 'M&M', 'ACR', 'Interviews']:
        paragraph.add_run(lecture['Time'] + ' - ' + lecture['Title'])
    else:
        paragraph.add_run(lecture['Time'] + ' - ' + lecture['Title'] + ' - ' + lecture['Presenter'] + ' - [' + lecture['Media'] + ']')
    if new_line:
        paragraph.add_run('\n')

def clean_name(name):
    return name.split(' (')[0]

def format_group_dict(group_dict, is_call):
    if is_call:
        if len(group_dict) == 1:
            return [[list(group_dict.keys())[0], 'All week']]
        else:
            return [[e, group_dict.get(e)] for e in group_dict]
    else:
        return [[e, group_dict.get(e)] for e in group_dict]

def add_group_run(paragraph, name):
    r = paragraph.add_run(f'{name}\n')
    r.bold = True
    r.underline = True

def get_suffix(i, group):
    suffix = '\n' if i != (len(group) - 1) else ''
    return suffix