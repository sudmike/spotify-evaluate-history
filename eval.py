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
