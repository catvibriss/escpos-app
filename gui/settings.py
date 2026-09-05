from .objects import Page

class Content(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(name="settings", *args, **kwargs)

    