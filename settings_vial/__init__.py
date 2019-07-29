import logging

from .settings_vial import Settings

__all__ = ["Settings"]

logging.getLogger(__name__).addHandler(logging.NullHandler())
