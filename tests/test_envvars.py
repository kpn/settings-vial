import pytest

from settings_vial import Settings


@pytest.fixture
def mock_environment(monkeypatch):
    env_dict = {
        "USER": "test_environment",
        "PREFIX_HASH": '{"dict": "test"}',
        "PREFIX_DEBUG": "true",
        "PREFIX_SOME_KEY_PREFIX_REPEATED": "nested",
    }

    for var, value in env_dict.items():
        monkeypatch.setenv(var, value)


class TestEnvironmentSettings:
    def test_load_environment_with_prefix(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        assert settings.DEBUG is True
        assert settings.HASH == {"dict": "test"}

    def test_load_environment_does_not_load_unprefixed_vars(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        with pytest.raises(AttributeError):
            settings.USER

    def test_load_environment_with_prefix_strips_out_prefix(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        with pytest.raises(AttributeError):
            settings.PREFIX_DEBUG

        assert settings.DEBUG is True

    def test_prefix_gets_stripped_once_only(self, mock_environment):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_env()

        assert settings.SOME_KEY_PREFIX_REPEATED == "nested"
