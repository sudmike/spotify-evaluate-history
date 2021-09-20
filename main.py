from process_json_file import get_entries_from_json_file


if __name__ == '__main__':
    entries = []
    entries += get_entries_from_json_file('StreamingHistoryXXX.json')

    for entry in entries:
        entry.print_all()
