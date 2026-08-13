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
        },

        # ------------------------------------------
        # PERSONALITY
        # ------------------------------------------

        "PERSONALITY_MODE": {
            "switch",
            "change",
            "set",
            "use"
        },

        "GET_PERSONALITY_MODE": {
            "what",
            "which",
            "current",
            "tell"
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
    # PERSONALITY MODES
    # ==================================================

    PERSONALITY_MODES = {

        # ------------------------------------------
        # NORMAL
        # ------------------------------------------

        "normal": "NORMAL",

        "default": "NORMAL",

        # ------------------------------------------
        # FAMILY
        # ------------------------------------------

        "family": "FAMILY",

        "friendly": "FAMILY",

        # ------------------------------------------
        # SARCASTIC
        # ------------------------------------------

        "sarcastic": "SARCASTIC",

        "sarcasm": "SARCASTIC",

        # ------------------------------------------
        # ROASTING
        # ------------------------------------------

        "roasting": "ROASTING",

        "roast": "ROASTING",

        # ------------------------------------------
        # ABUSIVE
        # ------------------------------------------

        "abusive": "ABUSIVE",

        # ------------------------------------------
        # MIXED
        # ------------------------------------------

        "mixed": "MIXED"
    }

    # ==================================================
    # GET MODE PHRASES
    # ==================================================

    GET_MODE_PHRASES = {

        "what mode are you in",

        "which mode are you in",

        "what is your mode",

        "what's your mode",

        "what is your current mode",

        "what's your current mode",

        "which is your current mode",

        "tell me your mode",

        "tell me your current mode",

        "what personality are you using",

        "which personality are you using",

        "what personality mode are you using",

        "which personality mode are you using",

        "what personality mode are you in",

        "which personality mode are you in",

        # ------------------------------------------
        # Voice-recognition-friendly variants
        # ------------------------------------------

        "which mode is your",

        "which top is your mode",

        "what mode is your"

    }

    # ==================================================
    # PERSONALITY MODE DETECTION
    # ==================================================

    def get_personality_mode(
        self,
        lemmas
    ):

        for lemma in lemmas:

            mode = (
                self.PERSONALITY_MODES.get(
                    lemma
                )
            )

            if mode:

                return mode

        return None

    # ==================================================
    # GET PERSONALITY QUESTION
    # ==================================================

    def is_get_personality_mode(
        self,
        text,
        lemmas
    ):

        text = (
            text
            .lower()
            .strip()
            .rstrip(
                "?!.,"
            )
        )

        # ------------------------------------------
        # Exact / phrase matches
        # ------------------------------------------

        for phrase in self.GET_MODE_PHRASES:

            if phrase in text:

                return True

        words = set(
            lemmas
        )

        # ------------------------------------------
        # Flexible voice variations
        # ------------------------------------------
        #
        # which mode are you in
        # what mode are you in
        # current mode
        # personality mode
        #

        has_mode = (
            "mode" in words
        )

        has_personality = (
            "personality" in words
        )

        has_question_word = bool(
            words
            & {
                "what",
                "which",
                "current",
                "tell"
            }
        )

        has_state_phrase = (
            "be" in words
            or
            "are" in words
            or
            "is" in words
        )

        if has_mode and (
            has_question_word
            or
            has_personality
        ):

            if (
                has_state_phrase
                or
                has_personality
                or
                "current" in words
            ):

                return True

        return False

    # ==================================================
    # CLASSIFY
    # ==================================================

    def classify(
        self,
        lemmas
    ):

        words = set(
            lemmas
        )

        # ==================================================
        # GET PERSONALITY MODE
        # ==================================================
        #
        # Check this before generic commands.
        #
        # Examples:
        #
        # "what mode are you in"
        # "which mode are you in"
        # "what is your current mode"
        #

        if self.is_get_personality_mode(
            " ".join(lemmas),
            lemmas
        ):

            return "GET_PERSONALITY_MODE"

        # ==================================================
        # PERSONALITY MODE
        # ==================================================
        #
        # Examples:
        #
        # switch to abusive mode
        # change to family mode
        # use sarcastic mode
        # set roasting mode
        #

        if words & self.VERBS[
            "PERSONALITY_MODE"
        ]:

            if (
                words
                & set(
                    self.PERSONALITY_MODES.keys()
                )
            ):

                return "PERSONALITY_MODE"

        # ==================================================
        # CLOSE APP
        # ==================================================

        if words & self.VERBS[
            "CLOSE_APP"
        ]:

            return "CLOSE_APP"

        # ==================================================
        # PLAY VIDEO
        # ==================================================

        if words & self.VERBS[
            "PLAY_VIDEO"
        ]:

            return "PLAY_VIDEO"

        # ==================================================
        # OPEN APP
        # ==================================================

        if words & self.VERBS[
            "OPEN_APP"
        ]:

            return "OPEN_APP"

        # ==================================================
        # SEARCH
        # ==================================================

        if words & self.VERBS[
            "SEARCH"
        ]:

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

        if words & self.VERBS[
            "CREATE"
        ]:

            if (
                words
                & self.OBJECTS[
                    "CREATE_FOLDER"
                ]
            ):

                return "CREATE_FOLDER"

            if (
                words
                & self.OBJECTS[
                    "CREATE_FILE"
                ]
            ):

                return "CREATE_FILE"

            if (
                words
                & self.OBJECTS[
                    "CREATE_PYTHON_PROJECT"
                ]
            ):

                return "CREATE_PYTHON_PROJECT"

        # ==================================================
        # UNKNOWN
        # ==================================================

        return None