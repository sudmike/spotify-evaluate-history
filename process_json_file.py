import json
import datetime
from history_entry import HistoryEntry


def get_entries_from_json_file(filename: str):
    with open(('./files/' + filename), encoding='utf8') as jsonFile:
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


def generate_json_file_from_entries(entries, filename='StreamingHistoryCombined'):

    objects = []

    for entry in entries:
        objects.append(
            {
                "endTime": entry.datetime_played.strftime('%Y-%m-%d %H:%M'),
                "artistName": entry.artist_name,
                "trackName": entry.track_name,
                "msPlayed": entry.ms_played
            }
        )

    objects_json = json.dumps(objects, indent=2)

    with open('./files/' + filename + '.json', 'w', encoding='utf8') as jsonFile:
        jsonFile.write(objects_json)
        jsonFile.close()
