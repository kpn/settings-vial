import pytest

from settings_vial import Settings


@pytest.fixture
def mock_envfile(tmp_path):
    tmp_file = tmp_path / "settings.env"
    lines = (
        "USER=test_environment",
        """PREFIX_ESCAPED_HASH='{"dict": "test"}'""",
        """PREFIX_UNESCAPED_HASH   =   {"dict": "test"}  """,
        "PREFIX_DEBUG=true",
        "PREFIX_SOME_KEY_PREFIX_REPEATED=nested",
        "PREFIX_MULTILINE_KEY='===BEGIN PUBLIC CERTIFICATE=== ",
        " it is a certificate value ",
        "===END PUBLIC CERTIFICATE==='",
    )
    data = "\n".join(lines)
    try:
        # Python2 requires unicode, so we need to convert
        data = data.decode("utf-8")
    except AttributeError:
        # Python3 does not have str.decode, but write_text accepts str, so no conversion necessary
        pass

    tmp_file.write_text(data)
    return str(tmp_file)


class TestEnvfileSettings:
    def test_load_envfile_with_prefix(self, mock_envfile):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_dotenv_file(mock_envfile)

        assert settings.DEBUG is True
        assert settings.ESCAPED_HASH == {"dict": "test"}
        assert settings.UNESCAPED_HASH == {"dict": "test"}
        assert settings.MULTILINE_KEY == (
            "===BEGIN PUBLIC CERTIFICATE=== \n" " it is a certificate value \n" "===END PUBLIC CERTIFICATE==="
        )

    def test_load_envfile_does_not_load_unprefixed_vars(self, mock_envfile):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_dotenv_file(mock_envfile)

        with pytest.raises(AttributeError):
            settings.USER

    def test_load_envfile_with_prefix_strips_out_prefix(self, mock_envfile):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_dotenv_file(mock_envfile)

        with pytest.raises(AttributeError):
            settings.PREFIX_DEBUG

        assert settings.DEBUG is True

    def test_prefix_gets_stripped_once_only(self, mock_envfile):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_dotenv_file(mock_envfile)

        assert settings.SOME_KEY_PREFIX_REPEATED == "nested"

    def test_as_dict(self, mock_envfile):
        settings = Settings(env_prefix="PREFIX_")
        settings.load_dotenv_file(mock_envfile)

        as_dict = settings.as_dict()
        assert as_dict == settings._config
        assert isinstance(as_dict, dict)
