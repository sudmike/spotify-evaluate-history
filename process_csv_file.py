import csv
from datetime import datetime


def _create_daily_listening_dictionary_from_entries(entries):
    dictionary = {}  # associative map with date and time played on date

    # calculate listening time per day
    for entry in entries:
        if entry.datetime_played.date() in dictionary:
            dictionary[entry.datetime_played.date()] += entry.ms_played
        else:
            dictionary[entry.datetime_played.date()] = entry.ms_played

    return dictionary


def generate_daily_listening_csv_file(entries):

    dictionary = _create_daily_listening_dictionary_from_entries(entries)

    # open a csv file and write results
    with open('./files/DailyListening.csv', 'w', encoding='UTF8', newline='') as csv_file:
        header = ['date', 'ms_played']
        writer = csv.writer(csv_file)

        writer.writerow(header)

        for key in dictionary:
            date = key
            ms_played = dictionary[key]
            data = [date, ms_played]
            writer.writerow(data)


def generate_weekly_listening_csv_file(entries):

    dictionary = _create_daily_listening_dictionary_from_entries(entries)

    weekly_list = {}

    for key in dictionary:
        date = key
        ms_played = dictionary[key]
        year = date.isocalendar()[0]
        week = date.isocalendar()[1]

        weak_key = str(year) + ' ' + str(week)

        if weak_key in weekly_list:
            weekly_list[weak_key][2] += ms_played
        else:
            weekly_list[weak_key] = [year, week, ms_played]

    # open a csv file and write results
    with open('./files/WeeklyListening.csv', 'w', encoding='UTF8', newline='') as csv_file:
        header = ['year', 'week', 'ms_played']
        writer = csv.writer(csv_file)

        writer.writerow(header)

        for key in weekly_list:
            data = weekly_list[key]
            writer.writerow(data)
