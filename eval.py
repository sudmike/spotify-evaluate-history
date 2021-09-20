from prettytable import PrettyTable
import calendar


def ms_to_hours(ms: int, rnd: int):
    return round((ms / 1000 / 60 / 60), rnd)


def last_day_of_month(year: int, month: int):
    return (calendar.monthrange(year, month))[1]


def evaluate_months(entries):

    month_array = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # [1] = january, [2] = february, ...

    # calculate total time for each month
    for entry in entries:
        month_array[entry.datetime_played.month] += entry.ms_played

    # initialise tables for results
    table_month = PrettyTable(['Month', 'Total [h]', 'Avg [h]'])
    table_month.title = 'Monthly results'

    table_year = PrettyTable(['Total [h]', 'Total [m]', 'Avg [h]'])
    table_year.title = 'Full year results'

    total_year = 0

    for month in range(1, 13):  # iterate through each month
        total_month = ms_to_hours(month_array[month], 2)
        avg_month = round(total_month / last_day_of_month(entries[0].datetime_played.year, month), 3)
        total_year += total_month

        table_month.add_row([month, total_month, avg_month])

    avg_year = round(total_year / 365, 3)
    avg_year_minutes = round(total_year * 60)

    table_year.add_row([total_year, avg_year_minutes, avg_year])

    print(table_month)
    print(table_year)


def evaluate_weekdays(entries):

    week_array = [0, 0, 0, 0, 0, 0, 0]  # [0] = monday, [1] = tuesday, ...
    nr_of_weeks = 51

    # calculate total time for each weekday
    for entry in entries:
        week_array[entry.datetime_played.weekday()] += entry.ms_played

    table_day_of_week = PrettyTable(['Day of Week', 'Total [h]', 'Avg [h]'])
    table_day_of_week.title = 'Day of week results'

    for day_of_week in range(0, 7):
        total_day_of_week = ms_to_hours(week_array[day_of_week], 2)
        avg_day_of_week = round(total_day_of_week / nr_of_weeks, 2)

        table_day_of_week.add_row([day_of_week, total_day_of_week, avg_day_of_week])

    print(table_day_of_week)

    table_weekday_vs_weekend = PrettyTable(['Type', 'Avg [h]'])
    table_weekday_vs_weekend.title = 'Weekday vs Weekend results'

    total_weekday = 0
    total_weekend = 0
    total_weekday_and_weekend = 0

    # calculate time for weekdays
    for i in range(0, 5):
        total_weekday += ms_to_hours(week_array[i], 2)

    # calculate avg time for weekends
    for i in range(5, 7):
        total_weekend += ms_to_hours(week_array[i], 2)

    # calculate avg time total
    for i in range(0, 7):
        total_weekday_and_weekend += ms_to_hours(week_array[i], 2)

    avg_weekday = round(total_weekday / nr_of_weeks / 5, 2)
    avg_weekend = round(total_weekend / nr_of_weeks / 2, 2)
    avg_weekday_and_weekend = round(total_weekday_and_weekend / nr_of_weeks / 7, 2)

    table_weekday_vs_weekend.add_rows(
        [
            ['Weekdays', avg_weekday],
            ['Weekends', avg_weekend],
            ['Both', avg_weekday_and_weekend]
        ]
    )

    print(table_weekday_vs_weekend)


def evaluate_extreme_days(entries):

    dictionary = {}  # associative map with date and time played on date
    array_max = []  # array of days with most listening time

    table_extreme_days = PrettyTable(['Day', 'Time listened [h]', 'Day of week'])
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
        array_max.append([max_key, dictionary[max_key]])
        del dictionary[max_key]

    # write days with most listening time into table
    for pair in array_max:
        date = pair[0]
        value = pair[1]
        table_extreme_days.add_row([date, ms_to_hours(value, 3), date.strftime('%A')])

    # display table
    print(table_extreme_days)


def evaluate_daily_average(entries):

    dictionary = {}  # associative map with date and time played on date
    bucket_hourly = [0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0]
    bucket_relative = [0, 0, 0, 0, 0, 0]

    table_hourly = PrettyTable(['Nr of hours', 'Days total', 'Days relative [%]', 'Days relative cum [%]'])
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
        value = dictionary[date]
        value = round(ms_to_hours(value, 2))
        bucket_hourly[value] += 1
        bucket_relative[_hour_to_relative(value)] += 1

    i = 0
    relative_cum = 0
    # write absolute bucket into table
    for oop in bucket_hourly:
        relative = oop / 365 * 100
        relative_cum += relative
        table_hourly.add_row([i, oop, round(relative, 2), round(100 - relative_cum, 2)])
        i += 1

    i = 0
    relative_cum = 0
    # write relative bucket into table
    for oop in bucket_relative:
        relative = oop / 365 * 100
        relative_cum += relative
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
        table_relative.add_row([category, oop, round(relative, 2)])
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
