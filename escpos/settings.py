from typing import Any

from .printer import SerialPrinter, resolve_esc_command
from .exceptions import UnavaliableFeature, InvalidProfile
from .utils import parse_command
from .const import GS

@resolve_esc_command("init", b"@")
def reset_printer(printer: SerialPrinter, _cmd: bytes):
    printer.send_esc(_cmd)

@resolve_esc_command("unidirectional_printing", b"U")
def set_unidirectional_printing(printer: SerialPrinter, enabled: bool, _cmd: bytes):
    printer.send_esc(_cmd + bytes([enabled]))

def set_asb(printer: SerialPrinter, key: int | bytes):
    if not printer.profile.is_asb_avaliable():
        raise UnavaliableFeature("asb", printer.profile.name)

    key = bytes([key]) if isinstance(key, int) else key

    cmd = GS + b"a" + key
    printer.send(cmd)

def send_custom_setting(printer: SerialPrinter, setting: str, value: Any):
    settings = printer.profile.get_custom_settings()
    profile_name = printer.profile.name

    # custom settings?
    if len(setting) == 0:
        raise UnavaliableFeature("custom settings", profile_name)

    # this exists?
    selected = next((st for st in settings if st["name"] == setting), None)
    if selected is None:
        raise UnavaliableFeature(setting, profile_name)

    # input correct?
    if selected["input_type"] == "bool":
        if value not in (0, 1, True, False):
            raise ValueError("incorrect input. expected: bool")

        value = bytes([value])    
        
    else:
        try:
            int_limit = int(selected["input_type"])
            if int_limit < 1:
                raise InvalidProfile(f"unknown or invalid input_type \"{selected["input_type"]}\" for custom setting \"{setting}\"." 
                                    "check your profile and try again")
            
            if not isinstance(value, int): 
                raise ValueError(f"incorrect input. expected: int, not {type(value)}")

            if not value in range(0, int_limit+1):
                raise ValueError(f"incorrect input. expected: int in [0, {int_limit}], not {value}")

            value = bytes([value])    

        except Exception as e:
            raise InvalidProfile(f"unknown or invalid input_type \"{selected["input_type"]}\" for custom setting \"{setting}\"." 
                                 f"check your profile and try again\n\noccured exception: {repr(e)}")

    # build and send command
    cmd = parse_command(selected["command"]) + value
    printer.send(cmd)