from .printer import SerialPrinter
from .const import LF

def send_text(printer: SerialPrinter, text: bytes):
    printer.send(text)

def print_text(printer: SerialPrinter, text: bytes):
    printer.send(text + LF)