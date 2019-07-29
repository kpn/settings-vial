"""
test_settings-vial
----------------------------------

Tests for `settings-vial` module.
"""

import pytest
from settings_vial import Settings
from settings_vial.exceptions import MissingOverrideKeysWarning, NotCallableWarning, UnsupportedSetTypeWarning


@pytest.fixture
def mock_environment(monkeypatch):
    env_dict = {
        "USER": "test_environment",
        "PREFIX_HASH": '{"dict": "test"}',
        "PREFIX_DEBUG": "true",
        "PREFIX_OVERRIDE_KEY_DEBUG": "false",
        "PREFIX_SOME_KEY_PREFIX_REPEATED": "nested",
    }

    for var, value in env_dict.items():
        monkeypatch.setenv(var, value)


@pytest.fixture
def override_keys_function():
    return lambda: ['KEY']


class TestEnvironmentSettings:
    def test_load_environment_with_prefix(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        with pytest.raises(AttributeError):
            settings.USER
        with pytest.raises(AttributeError):
            settings.PREFIX_DEBUG

        assert settings.DEBUG is True
        assert settings.HASH == {'dict': 'test'}

    def test_load_environment_with_override_keys(self, mock_environment, override_keys_function):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        settings.load_env()

        assert settings.DEBUG is False
        assert settings.HASH == {'dict': 'test'}

    def test_missing_missing_override_key_from_callable_raises_warning(
        self, mock_environment, override_keys_function, mocker
    ):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        mocker.patch.object(settings, 'override_keys_function')
        settings.override_keys_function.return_value = ['MISSING_KEY']
        settings.load_env()

        with pytest.warns(MissingOverrideKeysWarning):
            assert settings.DEBUG is True

        settings.override_keys_function.return_value = []
        assert settings.HASH == {'dict': 'test'}
        assert settings.DEBUG is True

    def test_override_keys_function_not_callable_raises_warning(self, mock_environment):
        settings = Settings("PREFIX_", "OVERRIDE_", ['KEY'])
        settings.load_env()

        with pytest.warns(NotCallableWarning):
            assert settings.DEBUG is True

    def test_override_keys_function_does_not_return_list_or_set_raises_warning(
        self, mock_environment, override_keys_function, mocker
    ):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        mocker.patch.object(settings, 'override_keys_function')
        settings.override_keys_function.return_value = "KEY1, KEY2"
        settings.load_env()

        with pytest.warns(UnsupportedSetTypeWarning):
            assert settings.HASH == {'dict': 'test'}
            assert settings.DEBUG is True

    def test_prefix_gets_stripped_once_only(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        assert settings.SOME_KEY_PREFIX_REPEATED == "nested"


class TestSettingsTypes:
    @pytest.fixture
    def mock_environment_types(self, monkeypatch):
        env_dict = {
            "PREFIX_STRING": "vial",
            "PREFIX_INT": "42",
            "PREFIX_FLOAT": "3.14",
            "PREFIX_LIST": '["string", 42, 3.14, {"dict": "test"}]',
            "PREFIX_DICT": '{"dict": "test"}',
            "PREFIX_BOOL": 'true',
            "PREFIX_NONE": 'null',
        }

        for var, value in env_dict.items():
            monkeypatch.setenv(var, value)

    @pytest.fixture
    def settings(self):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        return settings

    def test_setting_load_as_string(self, mock_environment_types, settings):
        assert isinstance(settings.STRING, str)
        assert settings.STRING == "vial"

    def test_setting_load_as_int(self, mock_environment_types, settings):
        assert isinstance(settings.INT, int)
        assert settings.INT == 42

    def test_setting_load_as_float(self, mock_environment_types, settings):
        assert isinstance(settings.FLOAT, float)
        assert settings.FLOAT == 3.14

    def test_setting_load_as_list(self, mock_environment_types, settings):
        assert isinstance(settings.LIST, list)
        assert settings.LIST == ["string", 42, 3.14, {"dict": "test"}]

    def test_setting_load_as_dict(self, mock_environment_types, settings):
        assert isinstance(settings.DICT, dict)
        assert settings.DICT == {"dict": "test"}

    def test_setting_load_as_bool(self, mock_environment_types, settings):
        assert isinstance(settings.BOOL, bool)
        assert settings.BOOL is True

    def test_setting_load_as_none(self, mock_environment_types, settings):
        assert settings.NONE is None
