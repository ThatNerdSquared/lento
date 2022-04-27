from lento.common.init_sequence import init_sequence
from lento.config import Config


def test_init_sequence_works_properly_darwin(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        tmp_path / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        tmp_path / "Library" / "Application Support" / "Lento"
    )

    assert not Config.SETTINGS_PATH.exists()
    assert not Config.APPDATA_PATH.exists()

    result = init_sequence()
    assert result
    assert Config.SETTINGS_PATH.exists()
    assert Config.APPDATA_PATH.exists()


def test_init_sequence_works_properly_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        tmp_path / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        tmp_path / "AppData" / "Local" / "Lento"
    )

    assert not Config.SETTINGS_PATH.exists()
    assert not Config.APPDATA_PATH.exists()

    result = init_sequence()
    assert result
    assert Config.SETTINGS_PATH.exists()
    assert Config.APPDATA_PATH.exists()


def test_init_sequence_does_not_overwrite_darwin(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        tmp_path / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        tmp_path / "Library" / "Application Support" / "Lento"
    )
    Config.SETTINGS_PATH.write_text("TEST_LENTO_SETTINGS")
    Config.APPDATA_PATH.mkdir(parents=True)

    assert Config.SETTINGS_PATH.exists()
    assert Config.APPDATA_PATH.exists()

    result = init_sequence()
    assert result is False
    assert Config.SETTINGS_PATH.read_text() == "TEST_LENTO_SETTINGS"
    assert Config.APPDATA_PATH.exists()


def test_init_sequence_does_not_overwrite_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        tmp_path / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        tmp_path / "AppData" / "Local" / "Lento"
    )
    Config.SETTINGS_PATH.write_text("TEST_LENTO_SETTINGS")
    Config.APPDATA_PATH.mkdir(parents=True)

    assert Config.SETTINGS_PATH.exists()
    assert Config.APPDATA_PATH.exists()

    result = init_sequence()
    assert result is False
    assert Config.SETTINGS_PATH.read_text() == "TEST_LENTO_SETTINGS"
    assert Config.APPDATA_PATH.exists()
