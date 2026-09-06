from .const import *
from .profile import Profile

def parse_command(command: str) -> bytes:
    """
    parses a command string and cleans it for app

    :param command: command from profile to parse
    """

    if not command.isascii():
        raise ValueError(f"command \"{command}\" is not ASCII. commands must contain only ASCII chars")

    command = command.split()

    if not command:
        raise ValueError("command is empty. check commands in your profile")
    
    basics = {"esc": ESC, "gs": GS, "dle": DLE, "eot": EOT, "enq": ENQ, 
              "sp": SP, "lf": LF, "ff": FF, "cr": CR}

    res = bytearray(0)

    for part in command:
        if part.isdigit():
            res += bytes([int(part)])

        elif part.lower() in basics:
            res += basics[part.lower()]

        else:
            res += part.encode("ascii")

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
        