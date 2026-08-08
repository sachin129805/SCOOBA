"""
==================================================
SCOOBA

AI Engine

Author: Sachin
==================================================
"""

from ai.nlp.processor import NLPProcessor
from ai.decision import Decision

from launcher.v4.resolver import ApplicationResolver


class AIEngine:

    def __init__(self):

        self.processor = NLPProcessor()

        self.app_resolver = ApplicationResolver()

    def think(self, text: str) -> Decision:

        # ---------------------------------
        # Speech Normalization
        # ---------------------------------

        text = text.lower().strip()

        replacements = {

            # WhatsApp
            "what's up": "whatsapp",
            "whats up": "whatsapp",
            "what up": "whatsapp",
            "what's app": "whatsapp",
            "whats app": "whatsapp",
            "what app": "whatsapp",
            "what sap": "whatsapp",
            "whatsup": "whatsapp",

            # LinkedIn
            "linked in": "linkedin",

            # Microsoft Office
            "power point": "powerpoint",
            "microsoft word": "word",
            "micro soft word": "word",
            "microsoft excel": "excel",
            "micro soft excel": "excel",

            # Development
            "vs code": "visual studio code",
            "visual studio": "visual studio code",
            "git hub": "github"
        }

        for wrong, correct in replacements.items():

            text = text.replace(
                wrong,
                correct
            )

        # ---------------------------------
        # Detect Browser Search Command
        # ---------------------------------
        #
        # Examples:
        #
        # "open youtube and search good day"
        # "open youtube and search for good day"
        # "youtube search python tutorial"
        #
        # These should become:
        #
        # intent = SEARCH
        # entity = youtube
        # action = search
        # query = good day
        # target = youtube
        #

        search_markers = [
            " and search for ",
            " and search ",
            " search for ",
            " search ",
            " and find ",
            " and look for "
        ]

        search_marker = None

        for marker in search_markers:

            if marker in text:

                search_marker = marker

                break

        # ---------------------------------
        # Handle SEARCH
        # ---------------------------------

        if search_marker:

            parts = text.split(
                search_marker,
                1
            )

            app_part = parts[0].strip()
            query_part = parts[1].strip()

            # Remove opening words
            for word in [
                "open ",
                "launch ",
                "start ",
                "run "
            ]:

                if app_part.startswith(word):

                    app_part = (
                        app_part[len(word):]
                        .strip()
                    )

                    break

            # ---------------------------------
            # Resolve Application
            # ---------------------------------

            app = self.app_resolver.resolve(
                app_part
            )

            # If the complete phrase doesn't
            # resolve, check individual words.
            if not app:

                for token in app_part.split():

                    app = self.app_resolver.resolve(
                        token
                    )

                    if app:

                        app_part = token.lower()

                        break

            decision = Decision()

            decision.intent = "SEARCH"

            decision.entity = app_part

            decision.action = "search"

            decision.query = query_part

            decision.target = app_part

            decision.confidence = (
                1.0
                if app
                else 0.5
            )

            # ---------------------------------
            # Debug
            # ---------------------------------

            print("\n========== AI DECISION ==========")

            print(
                f"Intent      : "
                f"{decision.intent}"
            )

            print(
                f"Entity      : "
                f"{decision.entity}"
            )

            print(
                f"Action      : "
                f"{decision.action}"
            )

            print(
                f"Query       : "
                f"{decision.query}"
            )

            print(
                f"Target      : "
                f"{decision.target}"
            )

            print(
                f"Confidence  : "
                f"{decision.confidence}"
            )

            print(
                "=================================\n"
            )

            return decision

        # ---------------------------------
        # NLP
        # ---------------------------------

        result = self.processor.process(
            text
        )

        decision = Decision()

        decision.intent = result["intent"]

        decision.entity = result["entity"]

        decision.query = result.get(
            "query"
        )

        decision.target = result.get(
            "target"
        )

        decision.action = result.get(
            "action"
        )

        decision.location = result.get(
            "location"
        )

        # ---------------------------------
        # Resolve Application
        # ---------------------------------

        if decision.intent == "OPEN_APP":

            # IMPORTANT:
            #
            # If NLP already detected an
            # application, preserve it.

            if not decision.entity:

                words = (
                    text
                    .replace("open", "")
                    .replace("launch", "")
                    .replace("start", "")
                    .replace("run", "")
                    .strip()
                )

                # ---------------------------------
                # Remove Search Portion
                # ---------------------------------

                for marker in search_markers:

                    if marker in words:

                        words = words.split(
                            marker,
                            1
                        )[0].strip()

                        break

                # ---------------------------------
                # Resolve Complete App Name
                # ---------------------------------

                app = self.app_resolver.resolve(
                    words
                )

                if app:

                    decision.entity = words

                else:

                    # ---------------------------------
                    # Resolve Individual Tokens
                    # ---------------------------------

                    for token in result["tokens"]:

                        app = self.app_resolver.resolve(
                            token
                        )

                        if app:

                            decision.entity = (
                                token.lower()
                            )

                            break

        # ---------------------------------
        # Default Action
        # ---------------------------------

        if not decision.action:

            if decision.intent == "OPEN_APP":

                decision.action = "open"

            elif decision.intent == "CREATE_FILE":

                decision.action = "create"

            elif decision.intent == "CREATE_FOLDER":

                decision.action = "create"

        # ---------------------------------
        # Confidence
        # ---------------------------------

        decision.confidence = (
            1.0
            if decision.intent
            else 0.0
        )

        # ---------------------------------
        # Debug
        # ---------------------------------

        print("\n========== AI DECISION ==========")

        print(
            f"Intent      : "
            f"{decision.intent}"
        )

        print(
            f"Entity      : "
            f"{decision.entity}"
        )

        print(
            f"Action      : "
            f"{decision.action}"
        )

        print(
            f"Query       : "
            f"{decision.query}"
        )

        print(
            f"Target      : "
            f"{decision.target}"
        )

        print(
            f"Location    : "
            f"{decision.location}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "=================================\n"
        )

        return decision