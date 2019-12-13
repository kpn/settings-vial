import pytest
from settings_vial import Settings
from settings_vial.exceptions import MissingOverrideKeysWarning, NotCallableWarning, UnsupportedSetTypeWarning


@pytest.fixture
def mock_environment(monkeypatch):
    env_dict = {
        "PREFIX_HASH": '{"dict": "test"}',
        "PREFIX_VALUE_3": "default-value-3",
        "PREFIX_DEBUG": "true",
        "PREFIX_OVERRIDE_KEY_DEBUG": "false",
        "PREFIX_SOME_KEY_PREFIX_REPEATED": "nested",
        "PREFIX_OVERRIDE_KEY1_VALUE_1": "key1-value-1",
        "PREFIX_OVERRIDE_KEY1_VALUE_2": "key1-value-2",
        "PREFIX_OVERRIDE_KEY2_VALUE_1": "key2-value-1",
    }

    for var, value in env_dict.items():
        monkeypatch.setenv(var, value)


def override_keys_function():
    return ["KEY"]


class TestEnvironmentSettings:
    def test_load_environment_with_override_keys(self, mock_environment):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        settings.load_env()

        assert settings.DEBUG is False
        assert settings.HASH == {"dict": "test"}

    def test_missing_missing_override_key_from_callable_raises_warning(self, mock_environment, mocker):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        mocker.patch.object(settings, "override_keys_function")
        settings.override_keys_function.return_value = ["MISSING_KEY"]
        settings.load_env()

        with pytest.warns(MissingOverrideKeysWarning):
            assert settings.DEBUG is True

        settings.override_keys_function.return_value = []
        assert settings.HASH == {"dict": "test"}
        assert settings.DEBUG is True

    def test_override_keys_function_not_callable_raises_warning(self, mock_environment):
        settings = Settings("PREFIX_", "OVERRIDE_", ["KEY"])
        settings.load_env()

        with pytest.warns(NotCallableWarning):
            assert settings.DEBUG is True

    def test_override_keys_function_does_not_return_list_or_set_raises_warning(self, mock_environment, mocker):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        mocker.patch.object(settings, "override_keys_function")
        settings.override_keys_function.return_value = "KEY1, KEY2"
        settings.load_env()

        with pytest.warns(UnsupportedSetTypeWarning):
            assert settings.HASH == {"dict": "test"}
            assert settings.DEBUG is True

    def test_override_keys_function_preserves_order_of_overrides(self, mock_environment, mocker):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function)
        mocker.patch.object(settings, "override_keys_function")
        settings.override_keys_function.return_value = ("KEY1", "KEY2")
        settings.load_env()
        assert settings.VALUE_1 == "key1-value-1"
        assert settings.VALUE_2 == "key1-value-2"
        assert settings.VALUE_3 == "default-value-3"

    def test_override_keys_reverse_lookup(self, mock_environment, mocker):
        settings = Settings("PREFIX_", "OVERRIDE_", override_keys_function, override_keys_reverse_lookup=True)
        mocker.patch.object(settings, "override_keys_function")
        settings.override_keys_function.return_value = ("KEY1", "KEY2")
        settings.load_env()
        assert settings.VALUE_1 == "key2-value-1"
        assert settings.VALUE_2 == "key1-value-2"
        assert settings.VALUE_3 == "default-value-3"
