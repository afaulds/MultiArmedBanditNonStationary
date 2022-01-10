import json


class Settings:
    
    values = None

    def get_value(key, default=None):
        Settings.__load()
        if key in Settings.values:
            return Settings.values[key]
        else:
            return default

    def __load():
        if Settings.values is None:
            with open("settings.json", "r") as infile:
                Settings.values = json.loads(infile.read())

