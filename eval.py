from prettytable import PrettyTable
import calendar


def ms_to_hours(ms: float):
    return ms / 1000 / 60 / 60


def ms_to_hours_rounded(ms: float, rnd: int):
    return round(ms_to_hours(ms), rnd)


def last_day_of_month(year: int, month: int):
    return (calendar.monthrange(year, month))[1]


def evaluate_months(entries):

    month_array = [0] * 12  # [0] = january, [1] = february, ...

    # calculate total time for each month
    for entry in entries:
        month_array[entry.datetime_played.month - 1] += entry.ms_played

    # initialise tables for results
    table_month = PrettyTable(['Month', 'Total [h]', 'Avg [h]'])
    table_month.title = 'Monthly results'

    table_year = PrettyTable(['Total [h]', 'Total [m]', 'Avg [h]'])
    table_year.title = 'Full year results'

    total_year_ms = 0

    for month in range(0, 12):  # iterate through each month
        total_month_ms = month_array[month]
        avg_month_ms = total_month_ms / last_day_of_month(entries[0].datetime_played.year, month + 1)
        total_year_ms += total_month_ms

        table_month.add_row([month + 1, ms_to_hours_rounded(total_month_ms, 2), ms_to_hours_rounded(avg_month_ms, 3)])

    avg_year_ms = total_year_ms / 365
    avg_year_minutes = round(ms_to_hours(total_year_ms) * 60)

    table_year.add_row([ms_to_hours_rounded(total_year_ms, 1), avg_year_minutes, ms_to_hours_rounded(avg_year_ms, 3)])

    print(table_month)
    print(table_year)


def evaluate_weekdays(entries):

    days_of_week_array = [0] * 7  # [0] = monday, [1] = tuesday, ...
    nr_of_weeks = 51

    # calculate total time for each weekday
    for entry in entries:
        days_of_week_array[entry.datetime_played.weekday()] += entry.ms_played

    table_day_of_week = PrettyTable(['Day of Week', 'Total [h]', 'Avg [h]'])
    table_day_of_week.title = 'Day of week results'

    for day_of_week in range(0, 7):
        total_ms = days_of_week_array[day_of_week]
        avg_ms = total_ms / nr_of_weeks

        table_day_of_week.add_row([day_of_week, ms_to_hours_rounded(total_ms, 2), ms_to_hours_rounded(avg_ms, 3)])

    print(table_day_of_week)

    table_weekday_vs_weekend = PrettyTable(['Type', 'Avg [h]'])
    table_weekday_vs_weekend.title = 'Weekday vs Weekend results'

    total_weekday_ms = 0
    total_weekend_ms = 0

    # calculate time for weekdays
    for day in range(0, 5):
        total_weekday_ms += days_of_week_array[day]

    # calculate avg time for weekends
    for day in range(5, 7):
        total_weekend_ms += days_of_week_array[day]

    # calculate avg time total
    total_weekday_and_weekend_ms = total_weekday_ms + total_weekend_ms

    # calculate averages
    avg_weekday_ms = total_weekday_ms / nr_of_weeks / 5
    avg_weekend_ms = total_weekend_ms / nr_of_weeks / 2
    avg_weekday_and_weekend_ms = total_weekday_and_weekend_ms / nr_of_weeks / 7

    table_weekday_vs_weekend.add_rows(
        [
            ['Weekdays', ms_to_hours_rounded(avg_weekday_ms, 2)],
            ['Weekends', ms_to_hours_rounded(avg_weekend_ms, 2)],
            ['Both', ms_to_hours_rounded(avg_weekday_and_weekend_ms, 2)]
        ]
    )

    print(table_weekday_vs_weekend)


def evaluate_extreme_days(entries):

    dictionary = {}  # associative map with date and time played on date
    array_extreme_days = []  # array of days with most listening time

    table_extreme_days = PrettyTable(['Date', 'Time listened [h]', 'Day of week'])
    table_extreme_days.title = 'Extreme days'

    # calculate listening time per day
    for entry in entries:
        if entry.datetime_played.date() in dictionary:
            dictionary[entry.datetime_played.date()] += entry.ms_played
        else:
            dictionary[entry.datetime_played.date()] = entry.ms_played

    # isolate days with most listening time
    for i in range(0, 15 if len(dictionary) > 15 else len(dictionary)):
        max_key = max(dictionary, key=dictionary.get)
        array_extreme_days.append([max_key, dictionary[max_key]])
        del dictionary[max_key]

    # write days with most listening time into table
    for date_listening_tuple in array_extreme_days:
        date = date_listening_tuple[0]
        listening_time = date_listening_tuple[1]
        table_extreme_days.add_row([date, ms_to_hours_rounded(listening_time, 3), date.strftime('%A')])

    # display table
    print(table_extreme_days)


def evaluate_daily_average(entries):

    dictionary = {}  # associative map with date and time played on date
    bucket_hourly = [0] * 24
    bucket_relative = [0] * 6

    table_hourly = PrettyTable(['Nr of hours', 'Days total', 'Days relative [%]', 'Days relative cumulative [%]'])
    table_hourly.title = 'Detailed hour for hour'
    table_relative = PrettyTable(['Categorisation', 'Days total', 'Days relative [%]'])
    table_relative.title = 'Categorised'

    # calculate listening time per day
    for entry in entries:
        if entry.datetime_played.date() in dictionary:
            dictionary[entry.datetime_played.date()] += entry.ms_played
        else:
            dictionary[entry.datetime_played.date()] = entry.ms_played

    # iterate through map and check what buckets days go into
    for date in dictionary:
        listening_time_ms = dictionary[date]
        listening_time_hours = ms_to_hours(listening_time_ms)
        bucket_hourly[round(listening_time_hours)] += 1
        bucket_relative[_hour_to_relative(listening_time_hours)] += 1

    i = 0
    percent_cumulative = 0
    num_of_dates = len(dictionary)
    # write absolute bucket into table
    for occurrences in bucket_hourly:
        percent = occurrences / num_of_dates * 100
        percent_cumulative += percent
        table_hourly.add_row([i, occurrences, round(percent, 2), round(100 - percent_cumulative, 2)])
        i += 1

    i = 0
    percent_cumulative = 0
    # write relative bucket into table
    for occurrences in bucket_relative:
        percent = occurrences / num_of_dates * 100
        percent_cumulative += percent
        category = ''
        if i == 0:
            category = 'basically nothing'
        elif i == 1:
            category = 'slow day'
        elif i == 2:
            category = 'average day'
        elif i == 3:
            category = 'intense day'
        elif i == 4:
            category = 'insane day'
        elif i == 5:
            category = 'WTF day'
        table_relative.add_row([category, occurrences, round(percent, 2)])
        i += 1

    print(table_hourly)
    print(table_relative)


def _hour_to_relative(hours_listened: int):
    if hours_listened < 2.5:
        return 0  # basically nothing
    elif hours_listened < 5:
        return 1  # slow day
    elif hours_listened < 7.5:
        return 2  # average day
    elif hours_listened < 10:
        return 3  # intense day
    elif hours_listened < 12.5:
        return 4  # insane day
    elif hours_listened >= 12.5:
        return 5  # WTF day
