import json
import warnings
from os import environ

from .exceptions import MissingOverrideKeysWarning, NotCallableWarning, UnsupportedSetTypeWarning


class Settings:
    r"""Settings from environment variables.

    :param env_prefix: prefix to be used when looking through the environment for variables
    :param override_prefix: prefix to be used when looking for overrideable variables
    :param override_callable: callable to be used when retrieving the set of keys to be overriden

    Usage::

        $ export MY_APP_TEST_VAR=42

        >>> from settings_vial import Settings
        >>> settings = Settings(env_prefix="MY_APP_")
        >>> settings.load_env()
        >>> settings.TEST_VAR
        42
    """

    def __init__(self, env_prefix, override_prefix=None, override_callable=None):
        self.env_prefix = env_prefix
        self.override_prefix = override_prefix
        self.override_callable = override_callable
        self._config = {}
        self._override_config = {}

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.__dict__)

    __str__ = __repr__

    def __getattr__(self, attr):
        if self.override_prefix and self.override_callable:
            override_set = self._load_override_set()

            if override_set - set(self._override_config):
                warnings.warn(
                    "There's no configuration with override keys {}".format(override_set - set(self._override_config)),
                    MissingOverrideKeysWarning,
                )

            for key in override_set:
                try:
                    return self._override_config[key][attr]
                except KeyError:
                    pass

        try:
            return self._config[attr]
        except KeyError:
            raise AttributeError("{} has no attribute {}".format(self, attr))

    def _load_override_set(self):
        if not callable(self.override_callable):
            warnings.warn("The callable provided is not a function", NotCallableWarning)
            return set()

        override_set = self.override_callable()

        if not isinstance(override_set, list) and not isinstance(override_set, set):
            warnings.warn("Override callable does not return a set or a list", UnsupportedSetTypeWarning)
            return set()

        return set(override_set)

    def load_env(self):
        """ Loads configuration from environment variables as json encoded.

        Will load all environment variables containing :param env_prefix: as a prefix and strip
        the prefix so you can access it through attributes normally: `settings.VAR`.

        If :param override_prefix: is provided it will also extract all settings containing this prefix
        into a separate dictionary but accessible within the same :class: `Settings <Settings>` object.
        The override prefix is also stripped out, and these dynamic settings will consider the first
        string under a `_` split to be its key.
        """
        for var, value in environ.items():
            if var.startswith(self.env_prefix):
                _, var_name = var.split(self.env_prefix, 1)
                try:
                    json_value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    json_value = value

                self._config.update({var_name: json_value})

        if self.override_prefix:
            self._load_overrides()

    def _load_overrides(self):
        vars_to_delete = []
        for var in self._config:
            if var.startswith(self.override_prefix):
                vars_to_delete.append(var)
                _, stripped_var_name = var.split(self.override_prefix, 1)
                override_key, var_name = stripped_var_name.split('_', 1)
                override_dict = {var_name: self._config[var]}
                try:
                    self._override_config[override_key].update(override_dict)
                except KeyError:
                    self._override_config[override_key] = override_dict

        for var in vars_to_delete:
            del self._config[var]
