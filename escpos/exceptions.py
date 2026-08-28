class CommandNotAvaliable(Exception):
    pass

class BasicNotAvaliable(Exception):
    pass

class InvalidProfile(Exception):
    pass

class MissedProfileField(InvalidProfile):
    def __init__(self, field: str, profile_id: str):
        """
        :param field: missed field
        :param profile_id: profile path or profile name
        """
        super().__init__(f"required field \"{field}\" missed in profile \"{profile_id}\"")