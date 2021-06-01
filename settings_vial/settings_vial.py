import copy
import json
import warnings
from os import environ

from dotenv import dotenv_values

from .exceptions import MissingOverrideKeysWarning, NotCallableWarning, UnsupportedSetTypeWarning

try:
    from json.decode import JSONDecodeError
except ImportError:
    # Python2.7 does not have this exception, it simply raises ValueError
    JSONDecodeError = ValueError


class Settings:
    r"""Settings from environment variables.

    :param env_prefix: prefix to be used when looking through the environment for variables
    :param override_prefix: prefix to be used when looking for overrideable variables
    :param override_keys_function: function returning a set of keys to be used as overrides

    Usage::

        $ export MY_APP_TEST_VAR=42
        $ echo 'MY_APP_SECRET=t0p5ecre+' > /tmp/secrets.env

        >>> from settings_vial import Settings
        >>> settings = Settings(env_prefix="MY_APP_")
        >>> settings.load_env()
        >>> settings.load_dotenv_file("/tmp/secrets.env")
        >>> settings.TEST_VAR
        42
        >>> settings.SECRET
        't0p5ecre+'
    """

    def __init__(
        self, env_prefix, override_prefix=None, override_keys_function=None, override_keys_reverse_lookup=False
    ):
        self.env_prefix = env_prefix
        self.override_prefix = override_prefix
        self.override_keys_function = override_keys_function
        self.override_keys_reverse_lookup = override_keys_reverse_lookup
        self._config = {}
        self._override_config = {}

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.__dict__)

    __str__ = __repr__

    def __getattr__(self, attr):
        if self.override_prefix and self.override_keys_function:
            override_keys = self._load_override_keys()

            if set(override_keys) - set(self._override_config):
                warnings.warn(
                    "There's no configuration with override keys {}".format(
                        set(override_keys) - set(self._override_config)
                    ),
                    MissingOverrideKeysWarning,
                )

            if self.override_keys_reverse_lookup:
                override_keys = reversed(override_keys)

            for key in override_keys:
                try:
                    return self._override_config[key][attr]
                except KeyError:
                    pass

        try:
            return self._config[attr]
        except KeyError:
            raise AttributeError("{} has no attribute {}".format(self, attr))

    def _load_override_keys(self):
        if not callable(self.override_keys_function):
            warnings.warn("The callable provided is not a function", NotCallableWarning)
            return tuple()

        override_keys = self.override_keys_function()

        if not isinstance(override_keys, (list, tuple)):
            warnings.warn("Override callable does not return a tuple or a list", UnsupportedSetTypeWarning)
            return tuple()

        return override_keys

    def load_env(self):
        r"""Loads configuration from environment variables as json encoded.

        Will load all environment variables containing **env_prefix** as a prefix and strip
        the prefix so you can access it through attributes normally: ``settings.VAR``.

        If **override_prefix** is provided it will also extract all settings containing this prefix
        into a separate dictionary but accessible within the same :class:`settings_vial.Settings <Settings>` object.
        The override prefix is also stripped out, and these dynamic settings will consider the first
        string under a ``_`` split to be its key.
        """
        self._load_dict(environ)

    def load_dotenv_file(self, path):
        """Loads configuration from .env files as json encoded values.

        Works the same way as ``load_env``, but reads values from .env file instead of environment variables.
        """
        self._load_dict(dotenv_values(dotenv_path=path))

    def _load_dict(self, _dict):
        for var, value in _dict.items():
            if var.startswith(self.env_prefix):
                _, var_name = var.split(self.env_prefix, 1)
                # This try/except is needed to catch plain strings, for all the other types the JSON Decoder
                # works as expected, but when trying to load a plain string it fails expecting it to be
                # surrounded with `{}`.
                try:
                    json_value = json.loads(value)
                except JSONDecodeError:
                    json_value = value

                self._config.update({var_name: json_value})

        if self.override_prefix:
            self._load_overrides()

    def _load_overrides(self):
        r"""Traverses through the already loaded prefixed environment variables and
        extracts the overridable ones.

        If any of the environment variables loaded contains **override_prefix** the prefix will be stripped
        and the variable moved from the main `_config` dictionary to `_override_config` and it will be placed under
        the key that is provided right next to the **override_prefix**, which is also stripped from the variable name.

        The `override_key` has to be a single string since the split is done in the first `_`.
        **OK:** PREFIX_OVERRIDE_KEY123_MY_VAR
        **Not OK:** PREFIX_OVERRIDE_KEY_123_MY_VAR
        """
        vars_to_delete = []
        for var in self._config:
            if var.startswith(self.override_prefix):
                vars_to_delete.append(var)
                _, stripped_var_name = var.split(self.override_prefix, 1)
                override_key, var_name = stripped_var_name.split("_", 1)
                override_dict = {var_name: self._config[var]}
                self._override_config.setdefault(override_key, {}).update(override_dict)

        for var in vars_to_delete:
            del self._config[var]

    def as_dict(self):
        return copy.deepcopy(self._config)
