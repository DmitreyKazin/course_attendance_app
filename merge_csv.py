#!/usr/bin/env python3
"""
This script merges all attendance csv files from webex
into a large csv file.
"""

import pandas as pd
import os
from datetime import datetime

def merge_all_csv(directory):
    """
    :param directory: directory that contains the participant files
    :return: creates csv file called all_meetings.csv
    """
    all_meetings = pd.DataFrame()
    total_meetings_time = 0
    appointments = 0

    # iterate over all participant files
    for file in os.listdir(directory):
        if file.startswith('participant'):

            # creating path to file
            file_path = os.path.join(directory, file)

            # reading data
            session = pd.read_csv(file_path, encoding='utf-16', sep='\t')

            # convert all names to lower case
            session['Name'] = session['Name'].str.lower()

            # calculating total meeting time
            meeting_start = datetime.strptime(session.loc[0, 'Meeting Start Time'].split('\"')[1], "%Y-%m-%d %H:%M:%S")
            meeting_end = datetime.strptime(session.loc[0, 'Meeting End Time'].split('\"')[1], "%Y-%m-%d %H:%M:%S")
            total_meeting_time = (meeting_end - meeting_start).total_seconds() / 60
            total_meetings_time += total_meeting_time

            # calculating attendance time
            meeting_date = session['Meeting End Time'].str.split()[0][0].split('"')[1]
            session[meeting_date] = session[['Attendance Duration']].apply(lambda time: time.str.split().str[0])
            session[meeting_date] = session[meeting_date].astype('int64')
            session_sub = pd.DataFrame(session.groupby('Name')[meeting_date].sum()).reset_index(level=0)

            # concatenation
            if all_meetings.empty:
                all_meetings = session_sub.copy()
            else:
                all_meetings = pd.merge(left=all_meetings, right=session_sub, on='Name', how='outer')

    all_meetings['Name'] = all_meetings['Name'].str.title()  # add back uppercase letters
    # save the output in the given directory
    all_meetings.to_csv(os.path.join(directory, 'all_meetings.csv'))
