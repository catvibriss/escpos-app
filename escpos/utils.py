from .const import *
from .profile import Profile

def parse_command(command: str) -> bytes:
    """
    parses a command string and cleans it for app

    :param command: command from profile to parse
    """

    if not command.isascii():
        raise ValueError(f"command \"{command}\" is not ASCII. commands must contain only ASCII chars")

    command = command.lower()
    cmd_splitted = command.split()

    if not cmd_splitted:
        raise ValueError("command is empty. check commands in your profile")
    
    basics = {"esc": ESC, "gs": GS, "dle": DLE}

    res = basics[cmd_splitted[0]] if cmd_splitted[0] in basics else cmd_splitted[0].encode("ascii")
    for other in cmd_splitted[1:]:
        res += other.encode("ascii")

    return res

def decode_asb(asb_profile: dict, data: bytes) -> dict:
    """
    decodes ASB from printer profile

    :param profile: ASB from printer profile
    :param data: bytes from ASB
    """

    if not isinstance(data, bytes):
        raise TypeError(f"ASB expected bytes, not {type(data)}")
    
    if len(data) != 4:
        raise ValueError("incorrect ASB lenght")

    response = {}

    for byte in range(4):
        bkey = f"b{byte+1}"
        if bkey not in asb_profile:
            continue

        for bit, name in asb_profile[bkey].items():
            response[name] = bool((data[byte] >> int(bit)) & 1)

    return response
        