from .exceptions import InvalidProfile, MissedProfileField
from .const import ESC, GS, DLE
import json

from dataclasses import dataclass

@dataclass
class CustomSetting:
    command: str
    input_type: str
    name: str
    description: str | None = None

def load_json(profile_path: str) -> dict:
    with open(profile_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

class Profile:
    def __init__(self, profile_file_path: str):
        self.profile_path = profile_file_path

        self.profile_json = None
        self.name = None
        self.manufacturer = None
        self.basics = []
        
        self._load()

    # init
    def _load(self):
        self.profile_json = load_json(self.profile_path)

        self._validate()

        self.basics = self.profile_json["basics"]

    def _validate(self):
        # contain name
        self.name = self.profile_json.get("name", None)
        if self.name is None:
            raise MissedProfileField("name", self.profile_path)

        # manufacturer bcs why not
        self.manufacturer = self.profile_json.get("manufacturer", None)

        # checks
        required = ["basics", "esc_commands", "esc_overwrites", "esc_customs", "papers", "asb"]
        for req in required:
            if req not in self.profile_json:
                raise MissedProfileField(req, self.name)

    # cmds
    def get_command_group(self, group: str):
        group = group.lower()

        if group not in self.basics:
            raise ValueError(f"this command group not avaliable for profile \"{self.name}\"")

        commands   = self.profile_json.get(f"{group}_commands", None) 
        overwrites = self.profile_json.get(f"{group}_overwrites", None)
        customs    = self.profile_json.get(f"{group}_customs", None)

        return commands, overwrites, customs

    # papers
    def get_papers(self):
        return self.profile_json.get("papers")

    # settings
    def get_custom_settings(self):
        cmds = self.profile_json.get("custom_settings", [])
        res = []
        for cmd in cmds:
            res.append(CustomSetting(**cmd))

        return res

    # asb
    def is_asb_avaliable(self):
        return self.profile_json["asb"]["avaliable"]

    def get_asb(self):
        return self.profile_json["asb"]