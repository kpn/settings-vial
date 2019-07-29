class NotCallableWarning(Warning):
    """A callable was expected"""

    pass


class UnsupportedSetTypeWarning(Warning):
    """A set or list was expected"""

    pass


class MissingOverrideKeysWarning(Warning):
    """An override key(s) given by the callable is not present"""

    pass
