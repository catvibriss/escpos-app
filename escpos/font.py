from .printer import SerialPrinter, resolve_esc_command
from .const import ESC, SP

def _formatting(cmd: bytes, param: int, text: bytes):
    return ESC + cmd + bytes([param]) + text + ESC + cmd + bytes([0])

@resolve_esc_command("bold", b"E")
def bold(printer: SerialPrinter, text: bytes, _cmd: bytes):
    return _formatting(_cmd, 1, text)

@resolve_esc_command("underline", b"-")
def underline(printer: SerialPrinter, text: bytes, _cmd: bytes):
    return _formatting(_cmd, 1, text)

@resolve_esc_command("double_strike", b"G")
def double_strike(printer: SerialPrinter, text: bytes, _cmd: bytes):
    return _formatting(_cmd, 1, text)

@resolve_esc_command("italic", b"4")
def italic(printer: SerialPrinter, text: bytes, _cmd: bytes):
    return _formatting(_cmd, 1, text)

@resolve_esc_command("char_spacing", SP)
def char_spacing(printer: SerialPrinter, space: int, text: bytes, _cmd: bytes):
    return _formatting(_cmd, space, text)

@resolve_esc_command("line_spacing", b"3")
def line_spacing(printer: SerialPrinter, space: int, text: bytes, _cmd: bytes):
    return ESC + _cmd + bytes([space]) + text

@resolve_esc_command("line_spacing_default", b"2")
def line_spacing_default(printer: SerialPrinter, text: bytes, _cmd: bytes):
    return ESC + _cmd + text

