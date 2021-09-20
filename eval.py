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
