import platform
import subprocess
from pathlib import Path
from unittest.mock import MagicMock

from daemon import lento_notif


def test_init_notif_works_properly():
    notif = lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": "LlamaAudio",
        }
    )
    assert notif.name == "LlamaName"
    assert notif.title == "LlamaTitle"
    assert notif.body == "LlamaBody"
    assert notif.audio_paths == "LlamaAudio"


def test_send_banner_works_properly_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    mock_subprocess = MagicMock()
    monkeypatch.setattr(subprocess, "Popen", mock_subprocess)
    lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": None,
        }
    ).send_banner()
    mock_subprocess.assert_called_once_with(
        [
            "osascript",
            "-e",
            """display notification "LlamaBody" with title "LlamaTitle\"""",  # noqa: E501
        ]
    )


def test_send_banner_works_properly_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    mock_notification = MagicMock()
    monkeypatch.setattr(lento_notif.notification, "notify", mock_notification)
    lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": None,
        }
    ).send_banner()
    mock_notification.assert_called_once_with(
        title="LlamaTitle", message="LlamaBody", app_name="Lento", timeout=10
    )


def test_play_audio_works_properly_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    mock_subprocess = MagicMock()
    monkeypatch.setattr(subprocess, "Popen", mock_subprocess)
    lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": {
                "llama_theme": str(Path("Users") / "LlamaLords" / "llama_theme.mp3"),
                "Daydream": str(Path("Users") / "marika_takeuchi" / "daydream.mp3"),
            },
        }
    ).play_audio()
    mock_subprocess.assert_any_call(
        ["afplay", str(Path("Users") / "LlamaLords" / "llama_theme.mp3")]
    )
    mock_subprocess.assert_any_call(
        ["afplay", str(Path("Users") / "marika_takeuchi" / "daydream.mp3")]
    )
    assert mock_subprocess.call_count == 2


def test_play_audio_works_properly_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    mock_pygame_load = MagicMock()
    mock_pygame_play = MagicMock()
    monkeypatch.setattr(lento_notif.mixer.music, "load", mock_pygame_load)
    monkeypatch.setattr(lento_notif.mixer.music, "play", mock_pygame_play)
    lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": {
                "llama_theme": str(Path("Users") / "LlamaLords" / "llama_theme.mp3"),
                "Daydream": str(Path("Users") / "marika_takeuchi" / "daydream.mp3"),
            },
        }
    ).play_audio()
    mock_pygame_load.assert_any_call(
        str(Path("Users") / "LlamaLords" / "llama_theme.mp3")
    )
    mock_pygame_load.assert_any_call(
        str(Path("Users") / "marika_takeuchi" / "daydream.mp3")
    )
    assert mock_pygame_load.call_count == 2
    assert mock_pygame_play.call_count == 2


def test_show_popup_works_properly(monkeypatch):
    mock_popup = MagicMock()
    monkeypatch.setattr(lento_notif.DaemonPrompt, "show_notif_popup", mock_popup)
    lento_notif.LentoNotif(
        {
            "name": "LlamaName",
            "title": "LlamaTitle",
            "body": "LlamaBody",
            "audio_paths": None,
        }
    ).show_notif_popup()
    mock_popup.assert_called_once_with("LlamaTitle", "LlamaBody")
