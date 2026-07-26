"""
==================================================
SCOOBA

Database Cleaner

Cleans launcher/apps.json

Author: Sachin
==================================================
"""

import json
from pathlib import Path

from launcher.validator import ApplicationValidator


DATABASE = Path("launcher/apps.json")


def main():

    validator = ApplicationValidator()

    with open(DATABASE, "r", encoding="utf-8") as f:
        apps = json.load(f)

    cleaned = {}

    removed = 0

    for name, path in apps.items():

        path = validator.clean_path(path)

        if not validator.is_valid(name, path):
            removed += 1
            continue

        cleaned[name] = path

    with open(DATABASE, "w", encoding="utf-8") as f:

        json.dump(
            dict(sorted(cleaned.items())),
            f,
            indent=4
        )

    print("\n========================================")
    print("Original Entries :", len(apps))
    print("Removed          :", removed)
    print("Remaining        :", len(cleaned))
    print("========================================")


if __name__ == "__main__":
    main()