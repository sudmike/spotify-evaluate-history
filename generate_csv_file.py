import csv


def generate_daily_listening_csv_file(entries):

    dictionary = {}  # associative map with date and time played on date

    # calculate listening time per day
    for entry in entries:
        if entry.datetime_played.date() in dictionary:
            dictionary[entry.datetime_played.date()] += entry.ms_played
        else:
            dictionary[entry.datetime_played.date()] = entry.ms_played

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
