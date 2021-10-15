import datetime
import numpy as np
import pandas as pd
from requests_html import HTMLSession

def get_html_qg(url, headers):
    render_time = 4
    timeout_time = 30
    with HTMLSession() as sesh:
        print('Accessing Qgenda...')
        response = sesh.get(url, headers=headers)
        print('Rendering schedule...')
        response.html.render(sleep=render_time, timeout=timeout_time)
        print('Finished rendering!')
        return response.html

def get_active_dates(html_qg):
    DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    dates = html_qg.find('#dateHeaders')[0].text.split('\n')
    for e in DAYS:
        while e in dates:
            dates.remove(e)
    temp_dates = []
    for i in range(0, len(dates), 2):
        temp_dates.append(dates[i] + ' ' + dates[i + 1] + ' ' + str(datetime.date.today().year))

    return pd.to_datetime(pd.Series(temp_dates))

def get_cell_text(grid_cell):
    data_cell = grid_cell.attrs.get('data-cell').split(',')
    return [data_cell[0], data_cell[1], grid_cell.text]

def get_names(html_qg, rows):
    return np.array(list(map(lambda x: x.attrs.get('title'), html_qg.find('.header-cell'))))[rows]

def make_df_qg(html_qg, color_resident, is_resident):
    n_rows = len(html_qg.find('.header-cell'))
    resident_rows = np.argwhere(list(map(lambda x: x.attrs.get('class')[-1] == color_resident, html_qg.find('.header-cell')))).flatten()
    attending_rows = np.setdiff1d(np.arange(n_rows), resident_rows)
    residents = get_names(html_qg, resident_rows)
    attendings = get_names(html_qg, attending_rows)
    i_names = residents if is_resident else attendings
    i_rows = resident_rows if is_resident else attending_rows

    df_qg = pd.DataFrame(index=i_rows, columns=get_active_dates(html_qg))

    df_cell_text = pd.DataFrame(list(map(lambda x: get_cell_text(x), html_qg.find('.grid-cell'))), columns=['Row', 'Col', 'Text'])
    df_cell_text['Row'] = df_cell_text['Row'].astype(int)
    df_cell_text['Col'] = df_cell_text['Col'].astype(int)

    for e in i_rows:
        df_qg.loc[e] = df_cell_text.loc[df_cell_text['Row'] == e, 'Text'].values
    df_qg = df_qg.set_index(i_names, drop=True)

    return df_qg

def get_dict_var(df_i, str_var, timeframe):
    ser_var = (df_i.loc[timeframe] == str_var).any(axis=0)
    persons = ser_var.index[ser_var.values].values
    output = {}
    for e in persons:
        ser_e = df_i.loc[timeframe, e] == str_var
        output.update({e: list(ser_e.index[ser_e.values].map(lambda x: str(x.year) + '-' + str(x.month) + '-' + str(x.day)).values)})
    return output