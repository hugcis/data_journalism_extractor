class EmptyModuleError(Exception):
    """ An Error raised when an empty module is used
    """
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__("An empty module was passed.\n" + message)


class UnknownModuleError(Exception):
    """ An Error raised when the a module isn't in the list
    of known modules
    """
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__("An unknown module was used.\n" + message)
