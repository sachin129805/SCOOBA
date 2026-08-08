"""
==================================================
SCOOBA

Intent Classifier 5.0

Author: Sachin
==================================================
"""


class IntentClassifier:

    VERBS = {

        "OPEN_APP": {
            "open",
            "launch",
            "start",
            "run"
        },

        "CLOSE_APP": {
            "close",
            "quit",
            "exit",
            "terminate"
        },

        "SEARCH": {
            "search",
            "find",
            "google",
            "lookup"
        },

        "PLAY_VIDEO": {
            "play",
            "watch"
        },

        "CREATE": {
            "create",
            "make",
            "generate",
            "build",
            "new"
        }
    }

    OBJECTS = {

        "CREATE_FOLDER": {
            "folder",
            "directory"
        },

        "CREATE_FILE": {
            "file",
            "document"
        },

        "CREATE_PYTHON_PROJECT": {
            "project",
            "python",
            "flask",
            "django",
            "fastapi"
        }
    }

    def classify(self, lemmas):

        words = set(lemmas)

        # -----------------------------
        # Search
        # -----------------------------

        if words & self.VERBS["SEARCH"]:

            return "SEARCH"

        # -----------------------------
        # Play Video
        # -----------------------------

        if words & self.VERBS["PLAY_VIDEO"]:

            return "PLAY_VIDEO"

        # -----------------------------
        # Open App
        # -----------------------------

        if words & self.VERBS["OPEN_APP"]:

            return "OPEN_APP"

        # -----------------------------
        # Close App
        # -----------------------------

        if words & self.VERBS["CLOSE_APP"]:

            return "CLOSE_APP"

        # -----------------------------
        # Greeting
        # -----------------------------

        if {"hi", "hello", "hey"} & words:

            return "GREETING"

        # -----------------------------
        # Create
        # -----------------------------

        if words & self.VERBS["CREATE"]:

            if words & self.OBJECTS["CREATE_FOLDER"]:

                return "CREATE_FOLDER"

            if words & self.OBJECTS["CREATE_FILE"]:

                return "CREATE_FILE"

            if words & self.OBJECTS["CREATE_PYTHON_PROJECT"]:

                return "CREATE_PYTHON_PROJECT"

        return None