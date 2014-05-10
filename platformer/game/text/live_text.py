from text import Text
from game.graphics import install_graphics_module
from sys import modules

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



def recognizer(graphics_type):
        """Recognizes whether this graphics type is handled by :class:`game.text.live_text.LiveText`."""
        return graphics_type == 'live text'

def factory(*args, **kwargs):
        """Returns a :class:`game.text.live_text.LiveText` for the given arguments."""
        # TODO The actual function creation should not occur in this function
        text_source = kwargs.pop('text_source')
        module_name = text_source[ : text_source.rfind('.')]
        function_name = text_source[text_source.rfind('.')+1 : ]
        text_source_function = getattr(modules[module_name], function_name)

        return LiveText(text_source_function, *args, **kwargs)

install_graphics_module(__name__)
