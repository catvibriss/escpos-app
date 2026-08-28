from .exceptions import InvalidProfile, MissedProfileField
from .const import ESC, GS, DLE
import json

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

    def parse_command(self, prof_cmd: str):
        """
        parses a command string from the profile and cleans it for app

        :param prof_cmd: command from profile to parse
        """

        if not prof_cmd.isascii():
            raise InvalidProfile(f"command \"{prof_cmd}\" is not ASCII. profile commands must contain only ASCII chars")

        prof_cmd = prof_cmd.lower()
        cmd_splitted = prof_cmd.split()

        if not cmd_splitted:
            raise InvalidProfile("command is empty. check commands in your profile")
        
        basics = {"esc": ESC, "gs": GS, "dle": DLE}

        res = basics[cmd_splitted[0]] if cmd_splitted[0] in basics else cmd_splitted[0].encode("ascii")
        for other in cmd_splitted[1:]:
            res += other.encode("ascii")

        return res

    def get_command_group(self, group: str):
        group = group.lower()

        if group not in self.basics:
            raise ValueError(f"this command group not avaliable for profile \"{self.name}\"")

        commands   = self.profile_json.get(f"{group}_commands", None) 
        overwrites = self.profile_json.get(f"{group}_overwrites", None)
        customs    = self.profile_json.get(f"{group}_customs", None)

        return commands, overwrites, customs

    def get_papers(self):
        papers = self.profile_json.get("papers")
        return papers
        
    def get_paper_selection_cmd(self):
        return self.parse_command(self.profile_json["papers"]["setup_command"])

    