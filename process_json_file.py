import json
import datetime
from history_entry import HistoryEntry


def get_entries_from_json_file(filename: str):
    with open(('./jsonFiles/' + filename), encoding='utf8') as jsonFile:
        json_objects = json.load(jsonFile)
        jsonFile.close()

    array = []

    for json_object in json_objects:
        history_entry = HistoryEntry(
            json_object['trackName'],
            json_object['artistName'],
            datetime.datetime(
                int(json_object['endTime'][0:4]),
                int(json_object['endTime'][5:7]),
                int(json_object['endTime'][8:10]),
                int(json_object['endTime'][11:13]),
                int(json_object['endTime'][14:16])
            ),
            json_object['msPlayed']
        )

        array.append(history_entry)

    return array
