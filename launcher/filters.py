"""
==================================================
SCOOBA

Executable Filters

Author: Sachin
==================================================
"""

import os


# Executables that should NEVER appear as launchable apps
BAD_EXE_NAMES = {

    "uninstall.exe",
    "unins000.exe",
    "unins001.exe",
    "setup.exe",
    "installer.exe",
    "update.exe",
    "updater.exe",
    "repair.exe",
    "helper.exe",
    "crashpad_handler.exe",
    "elevation_service.exe",
    "notification_helper.exe",
    "service.exe",
    "daemon.exe",
    "dxsetup.exe",
    "vcredist_x64.exe",
    "vcredist_x86.exe",
    "vc_redist.x64.exe",
    "vc_redist.x86.exe",
    "pythonw.exe",
    "pythonservice.exe"

}


# Folder names that usually contain internal binaries
BAD_FOLDERS = {

    "cache",
    "__pycache__",
    "temp",
    "tmp",
    "logs",
    "resources",
    "locales",
    "swiftshader",
    "installer",
    "installers",
    "redist",
    "redistributable",
    "runtime",
    "runtimes"

}


# Words that indicate an internal executable
BAD_WORDS = {

    "uninstall",
    "installer",
    "install",
    "update",
    "updater",
    "repair",
    "helper",
    "service",
    "crashpad",
    "redist",
    "redistributable",
    "telemetry",
    "diagnostic",
    "migration",
    "bootstrap"

}


def should_skip(path: str) -> bool:

    path = path.lower()

    exe = os.path.basename(path)

    if exe in BAD_EXE_NAMES:
        return True

    for folder in BAD_FOLDERS:

        if f"\\{folder}\\" in path:
            return True

    for word in BAD_WORDS:

        if word in exe:
            return True

    return False