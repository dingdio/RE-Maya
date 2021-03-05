import json
import os


class ToolSettings:
    def __init__(self, repopath, importFacePoses, DEFAULT_DIR_KEY, RECENT_FILES, RECENT_FILES_MAX):
        self.repopath = repopath
        self.importFacePoses = importFacePoses
        self.DEFAULT_DIR_KEY = DEFAULT_DIR_KEY
        self.RECENT_FILES = RECENT_FILES
        self.RECENT_FILES_MAX = RECENT_FILES_MAX
    @classmethod
    def from_json(cls, data):
        return cls(**data)

def get():
    dirpath, file = os.path.split(__file__)
    config_file = directory = dirpath+"\\config.json"

    with open(config_file) as config_file:
        jsondata = json.load(config_file)
        data = ToolSettings.from_json(jsondata)
        return data


def save(toolSettings):
    dirpath, file = os.path.split(__file__)
    config_file = directory = dirpath+"\\config.json"

    with open(config_file, "w") as file:
        file.write(json.dumps(toolSettings.__dict__,indent=2, sort_keys=True))