"""
==================================================
SCOOBA V4

Application Resolver

Author: Sachin
==================================================
"""

from rapidfuzz import process

from launcher.v4.database import ApplicationDatabase
from launcher.v4.scorer import ApplicationScorer


class ApplicationResolver:

    def __init__(self):

        self.db = ApplicationDatabase()

    def resolve(self, query: str):

        if not query:
            return None

        query = query.lower().strip()

        # ---------------------------------
        # Built-in Apps & Websites
        # ---------------------------------

        SPECIAL = {
            "linkedin": {
                "path": "linkedin",
                "source": "builtin"
            },
            "whatsapp": {
                "path": "whatsapp",
                "source": "builtin"
            },
            "youtube": {
                "path": "youtube",
                "source": "builtin"
            },
            "gmail": {
                "path": "gmail",
                "source": "builtin"
            },
            "chatgpt": {
                "path": "chatgpt",
                "source": "builtin"
            },
            "notepad": {
                "path": "notepad.exe",
                "source": "builtin"
            },
            "calculator": {
                "path": "calc.exe",
                "source": "builtin"
            },
            "paint": {
                "path": "mspaint.exe",
                "source": "builtin"
            }
        }

        if query in SPECIAL:
            return SPECIAL[query]

        apps = self.db.all()

        candidates = {
            name: data
            for name, data in apps.items()
            if ApplicationScorer.allowed(name)
        }

        # ---------------------------------
        # Exact Match
        # ---------------------------------

        if query in candidates:
            return candidates[query]

        # ---------------------------------
        # Starts With
        # ---------------------------------

        for name, data in candidates.items():

            if name.startswith(query):
                return data

        # ---------------------------------
        # Contains
        # ---------------------------------

        for name, data in candidates.items():

            if query in name:
                return data

        # ---------------------------------
        # Fuzzy Match
        # ---------------------------------

        match = process.extractOne(
            query,
            list(candidates.keys()),
            score_cutoff=85
        )

        if match:
            return candidates[match[0]]

        return None


if __name__ == "__main__":

    resolver = ApplicationResolver()

    while True:

        app = input("\nApplication : ")

        if app.lower() == "exit":
            break

        print(resolver.resolve(app))