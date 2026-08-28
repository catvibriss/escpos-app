from .printer import SerialPrinter, resolve_esc_command
from .utils import parse_command
from .exceptions import InvalidProfile

# paper feeding
@resolve_esc_command("paper_feed", b"J")
def feed_paper(printer: SerialPrinter, amount: int, _cmd: bytes):
    amount = max(0, min(255, amount))
    printer.send_esc(_cmd + bytes([amount]))

@resolve_esc_command("reverse_paper_feed", b"K")
def reverse_feed_paper(printer: SerialPrinter, amount: int, _cmd: bytes):
    amount = max(0, min(255, amount))
    printer.send_esc(_cmd + bytes([amount]))

@resolve_esc_command("feed_lines", b"d")
def print_and_feed_paper(printer: SerialPrinter, lines: int, _cmd: bytes):
    lines = max(0, min(255, lines))
    printer.send_esc(_cmd + bytes([lines]))

@resolve_esc_command("reverse_feed_lines", b"e")
def print_and_reverse_feed_paper(printer: SerialPrinter, lines: int, _cmd: bytes):
    lines = max(0, min(255, lines))
    printer.send_esc(_cmd + bytes([lines]))
 
# paper cut
@resolve_esc_command("partial_cut", b"i")
def partial_cut(printer: SerialPrinter, _cmd: bytes):
    printer.send_esc(_cmd)

@resolve_esc_command("dotted_partial_cut", b"m")
def dotted_partial_cut(printer: SerialPrinter, _cmd: bytes):
    printer.send_esc(_cmd)

# paper select
def select_paper(printer: SerialPrinter, choose: str):
    papers = printer.profile.get_papers()
    if len(papers["papers"]) == 0:
        raise InvalidProfile(f"invalid papers in profile \"{printer.profile.name}\"")

    cmd = parse_command(papers["setup_command"])

    selected = next((pr for pr in papers["papers"] if pr["id"] == choose), None)
    if selected is None:
        raise ValueError(f"paper \"{choose}\" not found in profile \"{printer.profile.name}\"")

    cmd += parse_command(selected["command"])

    printer.send(cmd)