"""
==================================================
SCOOBA

AI Engine

Author: Sachin
==================================================
"""

import re

from ai.nlp.processor import NLPProcessor
from ai.decision import Decision

from launcher.v4.resolver import ApplicationResolver


class AIEngine:

    def __init__(self):

        self.processor = NLPProcessor()

        self.app_resolver = ApplicationResolver()

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def normalize(self, text):

        text = text.lower().strip()

        replacements = {

            # ------------------------------------------
            # WhatsApp
            # ------------------------------------------

            "what's up": "whatsapp",
            "whats up": "whatsapp",
            "what up": "whatsapp",
            "what's app": "whatsapp",
            "whats app": "whatsapp",
            "what app": "whatsapp",
            "what sap": "whatsapp",
            "whatsup": "whatsapp",

            # ------------------------------------------
            # LinkedIn
            # ------------------------------------------

            "linked in": "linkedin",

            # ------------------------------------------
            # Microsoft Office
            # ------------------------------------------

            "power point": "powerpoint",

            "microsoft word": "word",
            "micro soft word": "word",

            "microsoft excel": "excel",
            "micro soft excel": "excel",

            # ------------------------------------------
            # Development
            # ------------------------------------------

            "vs code": "visual studio code",

            "visual studio": (
                "visual studio code"
            ),

            "git hub": "github"
        }

        for wrong, correct in replacements.items():

            text = text.replace(
                wrong,
                correct
            )

        # ==================================================
        # VOICE NORMALIZATION
        # ==================================================
        #
        # Examples:
        #
        # "on youtube search for minecraft"
        #
        # becomes:
        #
        # "search youtube for minecraft"
        #
        # ==================================================

        text = re.sub(
            r"^on\s+"
            r"(youtube|google|github|gmail|chatgpt)"
            r"\s+search\s+for\s+",
            r"search \1 for ",
            text
        )

        text = re.sub(
            r"^on\s+"
            r"(youtube|google|github|gmail|chatgpt)"
            r"\s+search\s+",
            r"search \1 ",
            text
        )

        # ==================================================
        # CLEAN EXTRA SPACES
        # ==================================================

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==================================================
    # CLEAN QUERY
    # ==================================================

    def clean_query(self, query):

        if not query:

            return query

        query = query.strip()

        # ------------------------------------------
        # Remove leading "for"
        # ------------------------------------------

        query = re.sub(
            r"^for\s+",
            "",
            query
        )

        # ------------------------------------------
        # Remove accidental leading "on"
        # ------------------------------------------

        query = re.sub(
            r"^on\s+",
            "",
            query
        )

        # ------------------------------------------
        # Remove punctuation
        # ------------------------------------------

        query = query.rstrip(
            ".,!?;:"
        ).strip()

        return query

    # ==================================================
    # MULTI-STEP DETECTION
    # ==================================================

    def is_multi_step(self, text):

        connectors = [

            " and search ",
            " and search for ",

            " and find ",
            " and look for ",

            " and play ",
            " and watch ",

            ", search ",
            ", search for ",

            ", find ",
            ", look for ",

            ", play ",
            ", watch "
        ]

        for connector in connectors:

            if connector in text:

                return True

        return False

    # ==================================================
    # SPLIT MULTI-STEP COMMAND
    # ==================================================

    def split_steps(self, text):

        # ------------------------------------------
        # Normalize ", and"
        # ------------------------------------------

        text = re.sub(
            r",\s+and\s+",
            " and ",
            text
        )

        # ------------------------------------------
        # Split only when "and" is followed by
        # another recognizable action.
        # ------------------------------------------

        pattern = (
            r"\s+and\s+"
            r"(?="
            r"search\b|"
            r"find\b|"
            r"look\s+for\b|"
            r"play\b|"
            r"watch\b|"
            r"open\b|"
            r"launch\b|"
            r"start\b|"
            r"run\b"
            r")"
        )

        parts = re.split(
            pattern,
            text
        )

        cleaned = []

        for part in parts:

            part = part.strip(
                " ,."
            )

            if part:

                cleaned.append(
                    part
                )

        return cleaned

    # ==================================================
    # SEARCH PARSER
    # ==================================================

    def parse_search(self, text):

        browser_sites = {

            "youtube",
            "google",
            "github",
            "gmail",
            "chatgpt"
        }

        # ==================================================
        # PATTERN 1
        #
        # search youtube for minecraft
        #
        # ==================================================

        match = re.match(
            r"^search\s+"
            r"(youtube|google|github|gmail|chatgpt)"
            r"\s+for\s+(.+)$",
            text
        )

        if match:

            return (
                match.group(1),
                self.clean_query(
                    match.group(2)
                )
            )

        # ==================================================
        # PATTERN 2
        #
        # youtube search for minecraft
        #
        # ==================================================

        match = re.match(
            r"^(youtube|google|github|gmail|chatgpt)"
            r"\s+search\s+for\s+(.+)$",
            text
        )

        if match:

            return (
                match.group(1),
                self.clean_query(
                    match.group(2)
                )
            )

        # ==================================================
        # PATTERN 3
        #
        # youtube for minecraft
        #
        # ==================================================

        match = re.match(
            r"^(youtube|google|github|gmail|chatgpt)"
            r"\s+for\s+(.+)$",
            text
        )

        if match:

            return (
                match.group(1),
                self.clean_query(
                    match.group(2)
                )
            )

        # ==================================================
        # PATTERN 4
        #
        # search for minecraft on youtube
        #
        # ==================================================

        match = re.match(
            r"^search\s+for\s+(.+?)"
            r"\s+on\s+"
            r"(youtube|google|github|gmail|chatgpt)$",
            text
        )

        if match:

            return (
                match.group(2),
                self.clean_query(
                    match.group(1)
                )
            )

        # ==================================================
        # PATTERN 5
        #
        # find minecraft on youtube
        #
        # ==================================================

        match = re.match(
            r"^(?:find|look\s+for)\s+(.+?)"
            r"\s+on\s+"
            r"(youtube|google|github|gmail|chatgpt)$",
            text
        )

        if match:

            return (
                match.group(2),
                self.clean_query(
                    match.group(1)
                )
            )

        # ==================================================
        # PATTERN 6
        #
        # search for minecraft
        #
        # Default = Google
        #
        # ==================================================

        match = re.match(
            r"^search\s+for\s+(.+)$",
            text
        )

        if match:

            return (
                "google",
                self.clean_query(
                    match.group(1)
                )
            )

        # ==================================================
        # PATTERN 7
        #
        # search minecraft
        #
        # Default = Google
        #
        # ==================================================

        match = re.match(
            r"^search\s+(.+)$",
            text
        )

        if match:

            query = self.clean_query(
                match.group(1)
            )

            # ------------------------------------------
            # Safety:
            #
            # Don't accidentally treat
            # "search youtube for minecraft"
            # as a Google query.
            # ------------------------------------------

            for site in browser_sites:

                if query.startswith(
                    site + " for "
                ):

                    return (
                        site,
                        self.clean_query(
                            query[
                                len(site) + 5:
                            ]
                        )
                    )

            return (
                "google",
                query
            )

        # ==================================================
        # PATTERN 8
        #
        # find minecraft
        #
        # Default = Google
        #
        # ==================================================

        match = re.match(
            r"^find\s+(.+)$",
            text
        )

        if match:

            return (
                "google",
                self.clean_query(
                    match.group(1)
                )
            )

        # ==================================================
        # PATTERN 9
        #
        # look for minecraft
        #
        # Default = Google
        #
        # ==================================================

        match = re.match(
            r"^look\s+for\s+(.+)$",
            text
        )

        if match:

            return (
                "google",
                self.clean_query(
                    match.group(1)
                )
            )

        return (
            None,
            None
        )

    # ==================================================
    # SINGLE COMMAND
    # ==================================================

    def think_single(self, text):

        text = self.normalize(
            text
        )

        # ==================================================
        # SEARCH
        # ==================================================

        target, query = (
            self.parse_search(
                text
            )
        )

        if target and query:

            decision = Decision()

            decision.intent = "SEARCH"

            decision.entity = target

            decision.action = "search"

            decision.query = query

            decision.target = target

            decision.command = text

            decision.confidence = 1.0

            return decision

        # ==================================================
        # NLP
        # ==================================================

        result = self.processor.process(
            text
        )

        decision = Decision()

        decision.intent = result.get(
            "intent"
        )

        decision.entity = result.get(
            "entity"
        )

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

        decision.position = result.get(
            "position"
        )

        decision.command = text

        # ==================================================
        # CLEAN NLP QUERY
        # ==================================================

        if decision.query:

            decision.query = (
                self.clean_query(
                    decision.query
                )
            )

        # ==================================================
        # APP RESOLUTION
        # ==================================================

        if decision.intent == "OPEN_APP":

            if not decision.entity:

                words = text

                for remove_word in [

                    "open",
                    "launch",
                    "start",
                    "run"

                ]:

                    words = words.replace(
                        remove_word,
                        ""
                    )

                words = words.strip()

                app = (
                    self.app_resolver.resolve(
                        words
                    )
                )

                if app:

                    decision.entity = words

                else:

                    for token in result.get(
                        "tokens",
                        []
                    ):

                        app = (
                            self.app_resolver.resolve(
                                token
                            )
                        )

                        if app:

                            decision.entity = (
                                token.lower()
                            )

                            break

        # ==================================================
        # DEFAULT ACTION
        # ==================================================

        if not decision.action:

            if decision.intent == "OPEN_APP":

                decision.action = "open"

            elif decision.intent == "CREATE_FILE":

                decision.action = "create"

            elif decision.intent == "CREATE_FOLDER":

                decision.action = "create"

            elif (
                decision.intent
                == "CREATE_PYTHON_PROJECT"
            ):

                decision.action = "create"

            elif decision.intent == "PLAY_VIDEO":

                decision.action = "play"

        # ==================================================
        # CONFIDENCE
        # ==================================================

        decision.confidence = (

            1.0
            if decision.intent
            else 0.0
        )

        return decision

    # ==================================================
    # MAIN THINK
    # ==================================================

    def think(self, text: str):

        text = self.normalize(
            text
        )

        # ==================================================
        # MULTI-STEP
        # ==================================================

        if self.is_multi_step(text):

            parts = self.split_steps(
                text
            )

            decisions = []

            for part in parts:

                decision = (
                    self.think_single(
                        part
                    )
                )

                if decision.intent:

                    decisions.append(
                        decision
                    )

            # ==================================================
            # CONTEXT INHERITANCE
            # ==================================================

            last_target = None

            last_query = None

            for decision in decisions:

                # ------------------------------------------
                # Target inheritance
                # ------------------------------------------

                if decision.target:

                    last_target = (
                        decision.target
                    )

                elif decision.intent in (

                    "SEARCH",
                    "PLAY_VIDEO"

                ):

                    if last_target:

                        decision.target = (
                            last_target
                        )

                        decision.entity = (
                            decision.entity
                            or last_target
                        )

                # ------------------------------------------
                # Query inheritance
                # ------------------------------------------

                if decision.query:

                    last_query = (
                        decision.query
                    )

                elif decision.intent == "PLAY_VIDEO":

                    if last_query:

                        decision.query = (
                            last_query
                        )

            # ==================================================
            # MAIN DECISION
            # ==================================================

            main_decision = (

                decisions[0]
                if decisions
                else Decision()
            )

            main_decision.steps = (
                decisions
            )

            main_decision.command = text

            main_decision.confidence = (

                min(
                    (
                        d.confidence
                        for d in decisions
                    ),
                    default=0.0
                )
            )

            # ==================================================
            # DEBUG
            # ==================================================

            print(
                "\n========== MULTI-STEP AI =========="
            )

            for i, decision in enumerate(
                decisions,
                start=1
            ):

                print(
                    f"\nStep {i}"
                )

                print(
                    f"Intent   : "
                    f"{decision.intent}"
                )

                print(
                    f"Entity   : "
                    f"{decision.entity}"
                )

                print(
                    f"Action   : "
                    f"{decision.action}"
                )

                print(
                    f"Query    : "
                    f"{decision.query}"
                )

                print(
                    f"Target   : "
                    f"{decision.target}"
                )

                print(
                    f"Position : "
                    f"{decision.position}"
                )

            print(
                "\n===================================\n"
            )

            return main_decision

        # ==================================================
        # SINGLE COMMAND
        # ==================================================

        decision = self.think_single(
            text
        )

        # ==================================================
        # DEBUG
        # ==================================================

        print(
            "\n========== AI DECISION =========="
        )

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
            f"Position    : "
            f"{decision.position}"
        )

        print(
            f"Location    : "
            f"{decision.location}"
        )

        print(
            f"Command     : "
            f"{decision.command}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "=================================\n"
        )

        return decision