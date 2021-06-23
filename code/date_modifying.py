import pandas as pd
from pandas.tseries.offsets import DateOffset
ts = pd.Timestamp('2020-10-07')
print(ts.weekday())
# modify the beginning dataframe to the first of the week
def modify_start_end_date(date, forward=True):
    '''

    :param date: datetime for the date to modify
    :param forward: a boolean that specified if the date is moving forward
    to the beginning next week or back to the end of previous week
    :return: modified datetime
    '''
    if forward:
        if date.weekday() != 0:
            offset = 7-ts.weekday()
            start_date = date + DateOffset(offset)
            return start_date
        else:
            return date
    else:
    # modify the end date of dataframe to the end of last week
        if date.weekday() != 0:
            offset = date.weekday()
            end_date = date - DateOffset(offset+1)
            return end_date
        else:
            return date
print(type(modify_start_end_date(ts, forward = False)))
