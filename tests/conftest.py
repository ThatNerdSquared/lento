import platform

collect_ignore = []
if platform.system() != "Windows":
    collect_ignore.append("test_macos_proxy_controller.py")
    collect_ignore.append("test_windows_proxy_controller.py")
