import threading
import queue
from dataclasses import dataclass, field

import serial

from functools import wraps
from .exceptions import CommandNotAvaliable

import json

@dataclass
class RequestData:
    size: int
    response: bytearray = field(default_factory=bytearray)
    req_event: threading.Event = field(default_factory=threading.Event)
    cancelled: bool = False

def load_profile(profile_path: str):
    with open(profile_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

class SerialPrinter:
    def __init__(self, port: str, profile: dict, serial_handler: callable = None):
        self.port = port
        self.profile =  profile

        self._serial = None

        self._serial_handler = serial_handler

        self._asb_enabled = False

        self._rx_monitor_running = False
        self._rx_thread = None
        self._rx_buffer = bytearray()

        self._pending_requests = queue.Queue()
        self._current_request: RequestData = None   # if not enought bytes in buffer 

    # user basics
    def connect(self):
        self._serial = serial.Serial(
            port = self.port,
            baudrate = 9600, 
            timeout = 0.1,
        ) 

        self._rx_monitor_running = True
        self._rx_thread = threading.Thread(target=self._rx_monitor, daemon=True)
        self._rx_thread.start()

    def send(self, data):
        if self._serial is None:
            raise RuntimeError("connect device first!")
        
        self._serial.write(data)
        self._on_tx(data)

    def request(self, data, timeout: float = 3):
        req = RequestData(size=2)

        self.send(data)

        self._pending_requests.put(req)
        if not req.req_event.wait(timeout=timeout):
            req.cancelled = True
            raise TimeoutError(f"serial request timeout: {data}")

        answer = bytes(req.response)

        self._on_rx(answer)
        return answer

    # rx work
    def _rx_monitor(self):
        while self._rx_monitor_running:
            data = self._serial.read(1024)
            if data:
                self._on_rx_bytes(data)

    def _on_rx_bytes(self, data):
        self._rx_buffer.extend(data)

        def is_asb(data: bytes) -> bool:
            # check asb mask
            if len(data) == 1:
                return (data[0] & 0b10010011) == 0b00010000

            if len(data) != 4:
                return False

            return (
                (data[0] & 0b10010011) == 0b00010000
                and
                (data[1] & 0b10010000) == 0
                and
                (data[2] & 0b10010000) == 0
                and
                (data[3] & 0b10010000) == 0
            )

        while self._rx_buffer:

            # asb check
            if self._asb_enabled:
                if is_asb(self._rx_buffer[0:1]):
                    if len(self._rx_buffer) < 4:
                        break

                    check = self._rx_buffer[:4]
                    if is_asb(check):
                        self._on_asb(bytes(self._rx_buffer[:4]))
                        del self._rx_buffer[:4]
                        continue
                
            # request check
            if self._current_request is None:
                try:
                    self._current_request = self._pending_requests.get_nowait()
                except queue.Empty:
                    self._on_garbage(self._rx_buffer.pop(0))
                    continue

            if self._current_request.cancelled:
                self._current_request = None
                continue

            self._current_request.response.append(self._rx_buffer.pop(0))
            if len(self._current_request.response) == self._current_request.size:
                self._current_request.req_event.set()
                self._current_request = None
            
    # serial monitor interface
    def _on_tx(self, tx_data):
        self._trigger_serial_handler(tx_data, "tx")

    def _on_rx(self, rx_data):
        self._trigger_serial_handler(rx_data, "rx")

    def _on_garbage(self, garbage):
        self._trigger_serial_handler(garbage, "garbage")
    
    def _on_asb(self, asb_data):
        self._trigger_serial_handler(asb_data, "asb")

    def _trigger_serial_handler(self, data: bytes, data_type: str):
        if self._serial_handler is None: return

        try:
            self._serial_handler(data_type, data)
        except Exception as e:
            print(repr(e))

def check_profile(command_name, command_type):
    def decorator(func):
        @wraps(func)
        def wrapper(printer: SerialPrinter, *args, **kwargs):

            override = None
            profile = printer.profile

            if command_type == "esc":
                if command_name in profile["esc_commands"]:
                    override = None

                elif command_name in profile["esc_overwrites"]:
                    override = profile["esc_overwrites"][command_name]

                else:
                    command = next((cmd for cmd in profile["esc_customs"] if cmd["name"] == command_name), None)
                    if command is None:
                        raise CommandNotAvaliable(f"ESC command \"{command_name}\" not avaliable for {profile["name"]}")
                    
                    override = command["command"]
                
            return func(printer, override, *args, **kwargs)
        return wrapper
    return decorator