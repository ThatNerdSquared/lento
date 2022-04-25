import platform
import pytest
import subprocess
try:
    import winsound
except ImportError:
    pass
from daemon import lento_notif
from daemon.lento_notif import LentoNotif
from unittest.mock import MagicMock


def test_init_notif_works_properly():
    notif = LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": "LlamaAudio"
    })
    assert notif.name == "LlamaName"
    assert notif.title == "LlamaTitle"
    assert notif.body == "LlamaBody"
    assert notif.audio_paths == "LlamaAudio"


def test_send_banner_works_properly_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    mock_subprocess = MagicMock()
    monkeypatch.setattr(subprocess, "Popen", mock_subprocess)
    LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": None
    }).send_banner()
    mock_subprocess.assert_called_once_with([
        "osascript",
        "-e",
        """display notification "LlamaBody" with title "LlamaTitle\""""  # noqa: E501
    ])


def test_send_banner_works_properly_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    mock_notification = MagicMock()
    monkeypatch.setattr(lento_notif.notification, "notify", mock_notification)
    LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": None
    }).send_banner()
    mock_notification.assert_called_once_with(
        title="LlamaTitle",
        message="LlamaBody",
        app_name="Lento",
        timeout=10
    )


def test_play_audio_works_properly_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    mock_subprocess = MagicMock()
    monkeypatch.setattr(subprocess, "Popen", mock_subprocess)
    LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": {
            "llama_theme": "/Users/LlamaLords/llama_theme.mp3",
            "Daydream": "/Users/marika_takeuchi/daydream.mp3"
        }
    }).play_audio()
    mock_subprocess.assert_any_call([
        "afplay",
        "/Users/LlamaLords/llama_theme.mp3"
    ])
    mock_subprocess.assert_any_call([
        "afplay",
        "/Users/marika_takeuchi/daydream.mp3"
    ])
    assert mock_subprocess.call_count == 2


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="`winsound` cannot be tested on non-Windows platforms"
)
def test_play_audio_works_properly_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    mock_winsound = MagicMock()
    monkeypatch.setattr(lento_notif.winsound, "PlaySound", mock_winsound)
    LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": {
            "llama_theme": "/Users/LlamaLords/llama_theme.mp3",
            "Daydream": "/Users/marika_takeuchi/daydream.mp3"
        }
    }).play_audio()
    mock_winsound.assert_any_call([
        "/Users/LlamaLords/llama_theme.mp3",
        winsound.SND_ASYNC
    ])
    mock_winsound.assert_any_call([
        "/Users/marika_takeuchi/daydream.mp3",
        winsound.SND_ASYNC
    ])
    assert mock_winsound.call_count == 2


def test_show_popup_works_properly(monkeypatch):
    mock_popup = MagicMock()
    monkeypatch.setattr(
        lento_notif.DaemonPrompt,
        "show_notif_popup",
        mock_popup
    )
    LentoNotif({
        "name": "LlamaName",
        "title": "LlamaTitle",
        "body": "LlamaBody",
        "audio_paths": None
    }).show_notif_popup()
    mock_popup.assert_called_once_with(
        "LlamaTitle",
        "LlamaBody"
    )
