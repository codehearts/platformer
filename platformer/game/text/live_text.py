from text import Text

class LiveText(Text):
        """A text label which updates its contents with the return value of a function.

        A LiveText object can be created by the graphics
        factory by specifying "live text" as the graphics type.

        Attributes:
                get_text_source (function): The source of the label's contents.
        """

        def __init__(self, get_text_source, *args, **kwargs):
                """Creates a new live text label that updates its contents with the return value of ``get_text_source``.

                Args:
                        get_text_source (function): A function which returns the contents for the text label when the label is updated.
                """
                super(LiveText, self).__init__(*args, **kwargs)

                self.get_text_source = get_text_source
                # TODO Leave the following commented out because other items might not have been initialized yet
                #self.update(0)

        def update(self, *args, **kwargs):
                """Updates the label with the returned value of the text source function."""
                self.text = self.get_text_source()
