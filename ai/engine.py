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
        # CONVERSATIONAL CONTEXT
        # ==================================================

        self.last_query = None
        self.last_target = None

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def normalize(self, text: str):

        text = (
            text
            .lower()
            .strip()
        )

        replacements = {

            "what's up": "whatsapp",
            "whats up": "whatsapp",
            "what up": "whatsapp",
            "what's app": "whatsapp",
            "whats app": "whatsapp",
            "what app": "whatsapp",
            "what sap": "whatsapp",
            "whatsup": "whatsapp",

            "linked in": "linkedin",

            "power point": "powerpoint",

            "microsoft word": "word",
            "micro soft word": "word",

            "microsoft excel": "excel",
            "micro soft excel": "excel",

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

        return text

    # ==================================================
    # MULTI-STEP DETECTION
    # ==================================================

    def is_multi_step(
        self,
        text: str
    ):

        text = (
            text
            .lower()
            .strip()
        )

        # --------------------------------------------------
        # Explicit connectors
        # --------------------------------------------------

        connectors = [

            " and ",
            " then ",
            " after that ",
            " followed by ",
            " next "

        ]

        if any(
            connector in text
            for connector in connectors
        ):

            return True

        # --------------------------------------------------
        # Natural action transitions
        #
        # Example:
        #
        # open youtube search for pokemon
        #
        # Example:
        #
        # open youtube search for pokemon
        # play the third video
        # --------------------------------------------------

        action_pattern = re.compile(
            r"\b("
            r"open|launch|start|run|"
            r"search|find|lookup|"
            r"play|watch|"
            r"create|make|generate|build|"
            r"close|quit|exit|terminate"
            r")\b"
        )

        matches = list(
            action_pattern.finditer(
                text
            )
        )

        return len(matches) >= 2

    # ==================================================
    # SPLIT MULTI-STEP COMMAND
    # ==================================================

    def split_steps(
        self,
        text: str
    ):

        text = (
            text
            .lower()
            .strip()
        )

        # ==================================================
        # NORMALIZE CONNECTORS
        # ==================================================

        text = re.sub(
            r"\s+after that\s+",
            " and ",
            text
        )

        text = re.sub(
            r"\s+followed by\s+",
            " and ",
            text
        )

        text = re.sub(
            r"\s+then\s+",
            " and ",
            text
        )

        text = re.sub(
            r"\s+next\s+",
            " and ",
            text
        )

        # ==================================================
        # EXPLICIT "AND"
        # ==================================================

        if " and " in text:

            parts = [

                part.strip()

                for part in text.split(
                    " and "
                )

                if part.strip()

            ]

            cleaned = []

            for part in parts:

                part = part.strip()

                for prefix in [

                    "then ",
                    "next ",
                    "after that ",
                    "followed by "

                ]:

                    if part.startswith(
                        prefix
                    ):

                        part = (
                            part[
                                len(prefix):
                            ]
                            .strip()
                        )

                if part:

                    cleaned.append(
                        part
                    )

            return cleaned

        # ==================================================
        # NATURAL ACTION SEGMENTATION
        # ==================================================

        action_regex = re.compile(
            r"\b("
            r"open|launch|start|run|"
            r"search|find|lookup|"
            r"play|watch|"
            r"create|make|generate|build|"
            r"close|quit|exit|terminate"
            r")\b"
        )

        matches = list(
            action_regex.finditer(
                text
            )
        )

        if len(matches) < 2:

            return [
                text
            ]

        # ==================================================
        # ACTION BOUNDARIES
        # ==================================================

        boundaries = []

        for index, match in enumerate(
            matches
        ):

            verb = match.group(1)

            start = match.start()

            # First action
            if index == 0:

                boundaries.append(
                    start
                )

                continue

            # --------------------------------------------------
            # SEARCH
            # --------------------------------------------------

            if verb in {

                "search",
                "find",
                "lookup"

            }:

                boundaries.append(
                    start
                )

                continue

            # --------------------------------------------------
            # PLAY / WATCH
            # --------------------------------------------------

            if verb in {

                "play",
                "watch"

            }:

                remaining = (
                    text[
                        match.end():
                    ]
                    .strip()
                )

                playback_indicators = (

                    "video",
                    "song",
                    "movie",
                    "result",
                    "track",
                    "episode",
                    "clip",

                    "the first",
                    "the second",
                    "the third",
                    "the fourth",
                    "the fifth",
                    "the sixth",
                    "the seventh",
                    "the eighth",
                    "the ninth",
                    "the tenth",

                    "first video",
                    "second video",
                    "third video",
                    "fourth video",
                    "fifth video",

                    "first result",
                    "second result",
                    "third result",
                    "fourth result",
                    "fifth result"

                )

                if any(
                    indicator in remaining
                    for indicator in
                    playback_indicators
                ):

                    boundaries.append(
                        start
                    )

                    continue

                # Generic "play X" after another action
                if index > 0:

                    boundaries.append(
                        start
                    )

                    continue

            # --------------------------------------------------
            # OPEN / CREATE / CLOSE
            # --------------------------------------------------

            if verb in {

                "open",
                "launch",
                "start",
                "run",

                "create",
                "make",
                "generate",
                "build",

                "close",
                "quit",
                "exit",
                "terminate"

            }:

                boundaries.append(
                    start
                )

        boundaries = sorted(
            set(boundaries)
        )

        if len(boundaries) < 2:

            return [
                text
            ]

        # ==================================================
        # BUILD COMMAND PARTS
        # ==================================================

        parts = []

        for index, start in enumerate(
            boundaries
        ):

            if (
                index + 1
                < len(boundaries)
            ):

                end = boundaries[
                    index + 1
                ]

            else:

                end = len(text)

            part = (
                text[
                    start:end
                ]
                .strip()
            )

            if part:

                parts.append(
                    part
                )

        return parts

    # ==================================================
    # CLEAN QUERY
    # ==================================================

    def clean_query(
        self,
        query
    ):

        if not query:

            return query

        query = (
            query
            .strip()
        )

        prefixes = [

            "for ",
            "about ",
            "on ",
            "regarding ",
            "related to "

        ]

        for prefix in prefixes:

            if query.startswith(
                prefix
            ):

                query = (
                    query[
                        len(prefix):
                    ]
                    .strip()
                )

                break

        return query

    # ==================================================
    # SINGLE COMMAND
    # ==================================================

    def think_single(
        self,
        text: str
    ):

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
        # QUERY CLEANING
        # ==================================================

        if decision.query:

            decision.query = (
                self.clean_query(
                    decision.query
                )
            )

        # ==================================================
        # PLAY VIDEO QUERY CLEANUP
        # ==================================================
        #
        # NLP can sometimes interpret:
        #
        # "play the 5th video"
        #
        # as:
        #
        # query = "the"
        #
        # "the" is not a search query.
        # ==================================================

        if decision.intent == "PLAY_VIDEO":

            if decision.query in {

                "the",
                "a",
                "an"

            }:

                decision.query = None

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

                words = (
                    words
                    .strip()
                )

                app = (
                    self.app_resolver.resolve(
                        words
                    )
                )

                if app:

                    decision.entity = (
                        words
                    )

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
    # EXPLICIT TARGET DETECTION
    # ==================================================

    def _find_explicit_target(
        self,
        command
    ):

        command = (
            command
            .lower()
            .strip()
        )

        words = command.split()

        targets = [

            "youtube",
            "google",
            "github",
            "gmail",
            "chatgpt",
            "linkedin",
            "whatsapp",
            "spotify",
            "instagram",
            "facebook",
            "twitter",
            "reddit",
            "amazon"

        ]

        for target in targets:

            if target in words:

                return target

        return None

    # ==================================================
    # UPDATE PERSISTENT CONTEXT
    # ==================================================

    def _update_context(
        self,
        decision
    ):

        # --------------------------------------------------
        # Save useful query
        # --------------------------------------------------

        if decision.query:

            cleaned = (
                self.clean_query(
                    decision.query
                )
            )

            if cleaned:

                self.last_query = (
                    cleaned
                )

        # --------------------------------------------------
        # Save target
        # --------------------------------------------------

        if decision.target:

            self.last_target = (
                decision.target
                .lower()
                .strip()
            )

        elif decision.entity:

            self.last_target = (
                decision.entity
                .lower()
                .strip()
            )

    # ==================================================
    # APPLY CONTEXT TO PLAY VIDEO
    # ==================================================

    def _apply_video_context(
        self,
        decision
    ):

        if decision.intent != "PLAY_VIDEO":

            return decision

        # --------------------------------------------------
        # Ignore invalid NLP query
        # --------------------------------------------------

        if decision.query in {

            "the",
            "a",
            "an"

        }:

            decision.query = None

        # --------------------------------------------------
        # Use previous search query
        # --------------------------------------------------

        if (
            not decision.query
            and self.last_query
        ):

            decision.query = (
                self.last_query
            )

        # --------------------------------------------------
        # Use previous target
        # --------------------------------------------------

        if (
            not decision.target
            and self.last_target
        ):

            decision.target = (
                self.last_target
            )

            decision.entity = (
                decision.entity
                or self.last_target
            )

        # --------------------------------------------------
        # Video defaults to YouTube
        # --------------------------------------------------

        if not decision.target:

            decision.target = (
                "youtube"
            )

        if not decision.entity:

            decision.entity = (
                decision.target
            )

        return decision

    # ==================================================
    # MAIN THINK
    # ==================================================

    def think(
        self,
        text: str
    ):

        # ==================================================
        # NORMALIZATION
        # ==================================================

        text = self.normalize(
            text
        )

        # ==================================================
        # MULTI-STEP
        # ==================================================

        if self.is_multi_step(
            text
        ):

            parts = self.split_steps(
                text
            )

            decisions = []

            # ==================================================
            # FIRST PASS
            # ==================================================

            for part in parts:

                decision = (
                    self.think_single(
                        part
                    )
                )

                if decision.intent:

                    decision.command = (
                        part
                    )

                    decisions.append(
                        decision
                    )

            # ==================================================
            # CONTEXT
            # ==================================================

            last_target = None
            last_query = None

            # ==================================================
            # SECOND PASS
            # ==================================================

            for decision in decisions:

                command = (
                    decision.command
                    or ""
                )

                command = (
                    command
                    .lower()
                    .strip()
                )

                explicit_target = (
                    self._find_explicit_target(
                        command
                    )
                )

                # ==================================================
                # OPEN APP
                # ==================================================

                if (
                    decision.intent
                    == "OPEN_APP"
                ):

                    if explicit_target:

                        decision.target = (
                            explicit_target
                        )

                        decision.entity = (
                            explicit_target
                        )

                        last_target = (
                            explicit_target
                        )

                    elif decision.entity:

                        last_target = (
                            decision.entity
                            .lower()
                            .strip()
                        )

                        decision.target = (
                            last_target
                        )

                # ==================================================
                # SEARCH
                # ==================================================

                elif (
                    decision.intent
                    == "SEARCH"
                ):

                    if explicit_target:

                        decision.target = (
                            explicit_target
                        )

                        decision.entity = (
                            explicit_target
                        )

                        last_target = (
                            explicit_target
                        )

                    elif last_target:

                        decision.target = (
                            last_target
                        )

                        decision.entity = (
                            last_target
                        )

                    else:

                        decision.target = (
                            "google"
                        )

                        decision.entity = (
                            "google"
                        )

                # ==================================================
                # PLAY VIDEO
                # ==================================================

                elif (
                    decision.intent
                    == "PLAY_VIDEO"
                ):

                    if explicit_target:

                        decision.target = (
                            explicit_target
                        )

                        decision.entity = (
                            explicit_target
                        )

                        last_target = (
                            explicit_target
                        )

                    elif last_target:

                        decision.target = (
                            last_target
                        )

                        decision.entity = (
                            last_target
                        )

                    else:

                        decision.target = (
                            "youtube"
                        )

                        decision.entity = (
                            "youtube"
                        )

                        last_target = (
                            "youtube"
                        )

                # ==================================================
                # QUERY INHERITANCE
                # ==================================================

                if decision.query:

                    decision.query = (
                        self.clean_query(
                            decision.query
                        )
                    )

                    # Do not remember meaningless
                    # determiner queries.

                    if decision.query in {

                        "the",
                        "a",
                        "an"

                    }:

                        decision.query = None

                    else:

                        last_query = (
                            decision.query
                        )

                elif (
                    decision.intent
                    == "PLAY_VIDEO"
                ):

                    if last_query:

                        decision.query = (
                            last_query
                        )

            # ==================================================
            # UPDATE PERSISTENT CONTEXT
            #
            # This is what allows:
            #
            # search for pokemon
            # play the fifth video
            #
            # across separate calls.
            # ==================================================

            for decision in decisions:

                self._update_context(
                    decision
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

            main_decision.command = (
                text
            )

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
        # APPLY PERSISTENT VIDEO CONTEXT
        # ==================================================

        decision = (
            self._apply_video_context(
                decision
            )
        )

        # ==================================================
        # UPDATE PERSISTENT CONTEXT
        # ==================================================

        self._update_context(
            decision
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