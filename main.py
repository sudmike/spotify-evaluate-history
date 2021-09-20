from process_json_file import get_entries_from_json_file
import eval


if __name__ == '__main__':
    entries = []
    entries += get_entries_from_json_file('StreamingHistoryXXX.json')

    eval.evaluate_months(entries)
