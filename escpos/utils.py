from .const import *

def parse_command(command: str):
    """
    parses a command string and cleans it for app

    :param prof_cmd: command from profile to parse
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