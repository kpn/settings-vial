class NotCallable(Warning):
    """A callable was expected"""

    pass


class UnsupportedSetType(Warning):
    """A set or list was expected"""

    pass


class MissingOverrideKeys(Warning):
    """An override key(s) given by the callable is not present"""

    pass
