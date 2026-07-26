"""
==================================================
SCOOBA

Application Database Cleaner

Author: Sachin
==================================================
"""

import json
from pathlib import Path


RAW_DB = Path("scanner/apps_raw.json")
CLEAN_DB = Path("scanner/apps_clean.json")


BLACKLIST = [

    "git",
    "mingw",
    "usr",
    "helper",
    "proxy",
    "service",
    "runtime",
    "redistributable",
    "driver",
    "update",
    "updater",
    "installer",
    "uninstall",
    "setup",
    "crash",
    "telemetry",
    "python",
    "node",
    "npm",
    "npx",
    "powershell",
    "command prompt",
    "cmd",

]


MIN_NAME_LENGTH = 3


def keep(name):

    name = name.lower()

    if len(name) < MIN_NAME_LENGTH:
        return False

    for word in BLACKLIST:

        if word in name:
            return False

    return True


def clean():

    with open(RAW_DB, "r", encoding="utf8") as f:

        apps = json.load(f)

    cleaned = {}

    for name, path in apps.items():

        if keep(name):

            cleaned[name] = path

    with open(CLEAN_DB, "w", encoding="utf8") as f:

        json.dump(
            dict(sorted(cleaned.items())),
            f,
            indent=4
        )

    print()

    print("=" * 40)

    print("RAW :", len(apps))

    print("CLEAN :", len(cleaned))

    print("=" * 40)


if __name__ == "__main__":

    clean()