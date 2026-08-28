class CommandNotAvaliable(Exception):
    pass

class BasicNotAvaliable(Exception):
    pass

class UnavaliableFeature(Exception):
    def __init__(self, feature: str, profile_id: str):
        """
        :param feature: feature
        :param profile_id: profile path or profile name
        """
        super().__init__(f"feature {feature} unavaliable for profile \"{profile_id}\". check profile or change feature")

class InvalidProfile(Exception):
    pass

class MissedProfileField(InvalidProfile):
    def __init__(self, field: str, profile_id: str):
        """
        :param field: missed field
        :param profile_id: profile path or profile name
        """
        super().__init__(f"required field \"{field}\" missed in profile \"{profile_id}\"")