"""
==================================================
SCOOBA

Intent Classifier

Author: Sachin
==================================================
"""


class IntentClassifier:

    # ==================================================
    # VERBS
    # ==================================================

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

    # ==================================================
    # OBJECTS
    # ==================================================

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

    # ==================================================
    # CLASSIFY
    # ==================================================

    def classify(self, lemmas):

        words = set(lemmas)

        # ==================================================
        # CLOSE APP
        # ==================================================
        #
        # Check explicit commands first.
        #

        if words & self.VERBS["CLOSE_APP"]:

            return "CLOSE_APP"

        # ==================================================
        # PLAY VIDEO
        # ==================================================

        if words & self.VERBS["PLAY_VIDEO"]:

            return "PLAY_VIDEO"

        # ==================================================
        # OPEN APP
        # ==================================================
        #
        # IMPORTANT:
        #
        # "open google"
        # "open youtube"
        # "launch github"
        #
        # must be OPEN_APP.
        #
        # Site names are entities, not actions.
        #

        if words & self.VERBS["OPEN_APP"]:

            return "OPEN_APP"

        # ==================================================
        # SEARCH
        # ==================================================
        #
        # IMPORTANT:
        #
        # "google" is NOT treated as a search verb anymore.
        #
        # The actual search verbs are:
        #
        # search
        # find
        # lookup
        #
        # "google" is handled as a browser target/entity
        # by the NLP processor.
        #

        if words & self.VERBS["SEARCH"]:

            return "SEARCH"

        # ==================================================
        # GREETING
        # ==================================================

        if {
            "hi",
            "hello",
            "hey"
        } & words:

            return "GREETING"

        # ==================================================
        # CREATE
        # ==================================================

        if words & self.VERBS["CREATE"]:

            if (
                words
                & self.OBJECTS["CREATE_FOLDER"]
            ):

                return "CREATE_FOLDER"

            if (
                words
                & self.OBJECTS["CREATE_FILE"]
            ):

                return "CREATE_FILE"

            if (
                words
                & self.OBJECTS["CREATE_PYTHON_PROJECT"]
            ):

                return "CREATE_PYTHON_PROJECT"

        # ==================================================
        # UNKNOWN
        # ==================================================

        return None