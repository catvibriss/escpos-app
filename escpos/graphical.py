from .printer import SerialPrinter, resolve_esc_command
from .const import ESC, LF, GS

from PIL import Image

def proceed_image(path: str, mode: int):
    image = Image.open(path).convert("RGB")

    # mono check
    colors = image.getcolors(maxcolors=3)
    if colors is None or not all(
        color in ((0, 0, 0), (255, 255, 255))
        for _, color in colors
    ):
        raise ValueError("expected TRUE monochrome image! only real white (255, 255, 255) and real black (0, 0, 0) colors")

    # "bit"map
    if mode in (0, 1):
        row_height = 8
    elif mode in (32, 33):
        row_height = 24

    width, height = image.size
    padded_width = (width + 7) // 8 * 8
    padded_height = (height + row_height - 1) // row_height * row_height

    if padded_height != height or padded_width != width:
        padded = Image.new("RGB", (padded_width, padded_height), "white")
        padded.paste(image, (0, 0))
        image = padded

    pixels = image.load()
    rows = []

    for y in range(0, padded_height, row_height):
        block = []

        for dy in range(row_height):
            for x in range(padded_width):
                r, g, b = pixels[x, y + dy]
                block.append(1 if (r, g, b) == (0, 0, 0) else 0)

        rows.append(block)

    return rows, padded_width

def escpos_rotation(bitmap, mode: int):
    if mode in (0, 1):
        row_height = 8
    elif mode in (32, 33):
        row_height = 24

    rows = []

    for block in bitmap:
        width = len(block) // row_height

        if len(block) % row_height != 0:
            raise ValueError("invalid bitmap block size")

        data = bytearray()

        for band in range(0, row_height, 8):
            for x in range(width):
                byte = 0

                for bit in range(8):
                    pixel = block[(band + bit) * width + x]

                    if pixel:
                        byte |= 1 << (7 - bit)

                data.append(byte)

        rows.append(bytes(data))

    return rows

@resolve_esc_command("print_bit_image", b"*")
def print_image(printer: SerialPrinter, mode: int, image_path: str, _cmd: bytes):

    # mode check
    if mode not in (0, 1, 32, 33):
        raise ValueError("unsupported mode! supported: (0, 1, 32, 33)")

    # image processing
    image_bitmap, width = proceed_image(image_path, mode)
    image_rows = escpos_rotation(image_bitmap, mode)

    # command args
    nL = width & 0xFF
    nH = (width >> 8) & 0xFF

    # row fix
    row_height = 8 if mode in (0,1) else 24
    printer.send_esc(b"3" + bytes([row_height*2]))

    # print image
    for row in image_rows:
        cmd = ESC + _cmd + bytes([mode, nL, nH]) + row
        printer.send(cmd + LF)

    # row fix
    printer.send_esc(b"2")