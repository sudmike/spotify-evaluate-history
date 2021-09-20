import datetime


class HistoryEntry:
    def __init__(self, track_name: str, artist_name: str, datetime_played: datetime, ms_played: int):
        self.track_name = track_name
        self.artist_name = artist_name
        self.datetime_played = datetime_played
        self.ms_played = ms_played

    def print_all(self):
        print('Entry: ',
              '\n  ', 'Track: ', self.track_name,
              '\n  ', 'Artist: ', self.artist_name,
              '\n  ', 'Time: ', self.datetime_played,
              '\n  ', 'Duration: ', self.ms_played, 'ms')
