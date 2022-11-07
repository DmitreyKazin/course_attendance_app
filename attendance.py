#!/usr/bin/env python3
"""
This script reads all attendance csv file from webex,
and summarize the information for each participant.
Prerequisite: Pandas library installed
"""

import pandas as pd
import os
from datetime import datetime


def data_eng(directory):
    """
    :param directory: directory that contains the participant files
    :return: creates csv file called all_meetings_submission.csv
             which summarize participants information
    """
    all_meetings = pd.DataFrame()
    total_meetings_time = 0
    flag = 0

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
            name = 'Attendance' + str(flag)
            flag += 1
            session[name] = session[['Attendance Duration']].apply(lambda time: time.str.split().str[0])
            session[name] = session[name].astype('int64')
            session_sub = pd.DataFrame(session.groupby('Name')[name].sum()).reset_index(level=0)

            # outer join
            if all_meetings.empty:
                all_meetings = session_sub.copy()
            else:
                all_meetings = pd.merge(left=all_meetings, right=session_sub, on='Name', how='outer')

    # calculating total course attendance time & percentage
    attendance_columns = all_meetings.drop('Name', axis=1).columns
    all_meetings['Total_Min'] = all_meetings.loc[:, attendance_columns].sum(axis=1).astype('int64')
    all_meetings['Total_Percentage'] = round(all_meetings['Total_Min'] / total_meetings_time * 100, 2)
    all_meetings['Name'] = all_meetings['Name'].str.title()  # add back uppercase letters

    # formatting final result
    all_meetings_sub = all_meetings[['Name', 'Total_Min', 'Total_Percentage']]

    # save the output in the given directory
    all_meetings_sub.to_csv(os.path.join(directory, 'all_meetings_submission.csv'))
