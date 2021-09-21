from process_json_file import get_entries_from_json_file
from generate_csv_file import generate_daily_listening_csv_file
import eval


if __name__ == '__main__':
    entries = []
    entries += get_entries_from_json_file('StreamingHistoryXXX.json')

    # eval.evaluate_months(entries)
    # eval.evaluate_weekdays(entries)
    # eval.evaluate_extreme_days(entries)
    # eval.evaluate_daily_average(entries)

    generate_daily_listening_csv_file(entries)
