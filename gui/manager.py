from escpos.printer import SerialPrinter
from escpos.profile import Profile

class ProfileMissed(Exception):
    pass

class AppManager:
    def __init__(self, printer: SerialPrinter | None = None):
        self.printer = printer
        self._printer_conn = False

        self.printer_profile = None

        self._refreshables_objects = []

    def register_refreshable(self, obj):
        self._refreshables_objects.append(obj)

    def refresh(self):
        for obj in self._refreshables_objects:
            obj.refresh()

    def printer_connect(self, port: str, profile: Profile | None = None):
        if profile is None:
            if self.printer_profile is None:
                raise ProfileMissed("select profile and try to connect again")
            else:
                profile = self.printer_profile

        self.printer.connect(port, profile)
        self._printer_conn = True
        self.refresh()

    def printer_disconnect(self):
        self._printer_conn = False
        self.refresh()

    @property
    def printer_connected(self):
        return self._printer_conn

    def set_printer_profile(self, profile: Profile):
        self.printer_profile = profile
