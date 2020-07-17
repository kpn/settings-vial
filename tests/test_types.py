import pytest

from settings_vial import Settings


@pytest.fixture
def mock_environment_types(monkeypatch):
    env_dict = {
        "PREFIX_STRING": "vial",
        "PREFIX_INT": "42",
        "PREFIX_FLOAT": "3.14",
        "PREFIX_LIST": '["string", 42, 3.14, {"dict": "test"}]',
        "PREFIX_DICT": '{"dict": "test"}',
        "PREFIX_BOOL": "true",
        "PREFIX_NONE": "null",
    }

    for var, value in env_dict.items():
        monkeypatch.setenv(var, value)


@pytest.fixture
def settings():
    settings = Settings(env_prefix="PREFIX_")
    settings.load_env()

    return settings


class TestSettingsTypes:
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
