import os
import numpy as np
import pandas as pd

from . import functions as funcs
from . import global_vars as globals

def fill_dates(df_i):
    e = df_i.loc[0, 'Date']
    for i in range(df_i.shape[0]):
        if df_i.loc[i, 'Date'] is np.nan:
            df_i.loc[i, 'Date'] = e
        else:
            e = df_i.loc[i, 'Date']

def get_weekly_lectures():
    df = pd.read_csv(os.path.join(globals.PATH_ASSETS, globals.FILENAME_SCHEDULE))
    fill_dates(df)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date', drop=True)

    week_dates = funcs.get_next_week()
    weekly_didactic_dates = week_dates[[e in df.index.map(lambda x: x.date()) for e in week_dates]]

    return df.loc[weekly_didactic_dates, ['Event', 'Time', 'Title', 'Presenter', 'Media']]