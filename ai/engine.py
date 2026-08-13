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

            # ==========================================
            # PERSONALITY MODE SPEECH CORRECTIONS
            # ==========================================

            "switch to abuse your mode": "switch to abusive mode",
            "switch to abuse your": "switch to abusive",
            "abuse your mode": "abusive mode",
            "abuse your": "abusive",
            "abuse mode": "abusive mode",

            # ==========================================
            # OTHER CORRECTIONS
            # ==========================================

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

            "visual studio": "visual studio code",

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

    def is_multi_step(self, text: str):

        markers = [

            " and ",
            " then ",
            " after that ",
            " followed by ",
            " next "
        ]

        return any(
            marker in text
            for marker in markers
        )

    # ==================================================
    # SPLIT MULTI-STEP COMMAND
    # ==================================================

    def split_steps(self, text: str):

        replacements = [

            " after that ",
            " followed by ",
            " then ",
            " next "
        ]

        for replacement in replacements:

            text = text.replace(
                replacement,
                " and "
            )

        parts = [

            part.strip()

            for part in text.split(" and ")

            if part.strip()
        ]

        return parts

    # ==================================================
    # CLEAN QUERY
    # ==================================================

    def clean_query(self, query):

        if not query:

            return query

        query = query.strip()

        prefixes = [

            "for ",
            "about ",
            "on ",
            "regarding ",
            "related to "
        ]

        for prefix in prefixes:

            if query.startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return query

    # ==================================================
    # SINGLE COMMAND
    # ==================================================

    def think_single(self, text: str):

        # ==================================================
        # NLP PROCESSING
        # ==================================================

        result = self.processor.process(
            text
        )

        decision = Decision()

        # ==================================================
        # BASIC DECISION DATA
        # ==================================================

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

        # ==================================================
        # PERSONALITY MODE
        # ==================================================

        decision.personality_mode = result.get(
            "personality_mode"
        )

        decision.command = text

        # ==================================================
        # CLEAN QUERY
        # ==================================================

        if decision.query:

            decision.query = self.clean_query(
                decision.query
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

                app = self.app_resolver.resolve(
                    words
                )

                if app:

                    decision.entity = words

                else:

                    for token in result.get(
                        "tokens",
                        []
                    ):

                        app = self.app_resolver.resolve(
                            token
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

            elif decision.intent == "CONVERSATION":

                decision.action = "chat"

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
    # FIND EXPLICIT TARGET
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
    # MAIN THINK
    # ==================================================

    def think(self, text: str):

        # ==================================================
        # NORMALIZE
        # ==================================================

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

            # ==============================================
            # FIRST PASS
            # ==============================================

            for part in parts:

                decision = self.think_single(
                    part
                )

                if decision.intent:

                    decision.command = part

                    decisions.append(
                        decision
                    )

            # ==============================================
            # CONTEXT VARIABLES
            # ==============================================

            last_target = None
            last_query = None

            # ==============================================
            # SECOND PASS
            # ==============================================

            for decision in decisions:

                command = (
                    decision.command
                    or ""
                )

                explicit_target = (
                    self._find_explicit_target(
                        command
                    )
                )

                # ==========================================
                # OPEN APP
                # ==========================================

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

                # ==========================================
                # SEARCH
                # ==========================================

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

                # ==========================================
                # PLAY VIDEO
                # ==========================================

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

                # ==========================================
                # QUERY INHERITANCE
                # ==========================================

                if decision.query:

                    decision.query = self.clean_query(
                        decision.query
                    )

                    last_query = (
                        decision.query
                    )

                elif (
                    decision.intent
                    == "PLAY_VIDEO"
                    and last_query
                ):

                    decision.query = (
                        last_query
                    )

            # ==============================================
            # MAIN DECISION
            # ==============================================

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

            # ==============================================
            # DEBUG
            # ==============================================

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
                    f"Intent   : {decision.intent}"
                )

                print(
                    f"Entity   : {decision.entity}"
                )

                print(
                    f"Action   : {decision.action}"
                )

                print(
                    f"Query    : {decision.query}"
                )

                print(
                    f"Target   : {decision.target}"
                )

                print(
                    f"Position : {decision.position}"
                )

                print(
                    f"Mode     : "
                    f"{getattr(decision, 'personality_mode', None)}"
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
        # CONVERSATION FALLBACK
        # ==================================================

        if not decision.intent:

            decision.intent = (
                "CONVERSATION"
            )

            decision.action = (
                "chat"
            )

            decision.confidence = 1.0

        # ==================================================
        # DEBUG
        # ==================================================

        print(
            "\n========== AI DECISION =========="
        )

        print(
            f"Intent      : {decision.intent}"
        )

        print(
            f"Entity      : {decision.entity}"
        )

        print(
            f"Action      : {decision.action}"
        )

        print(
            f"Query       : {decision.query}"
        )

        print(
            f"Target      : {decision.target}"
        )

        print(
            f"Position    : {decision.position}"
        )

        print(
            f"Location    : {decision.location}"
        )

        print(
            f"Mode        : "
            f"{getattr(decision, 'personality_mode', None)}"
        )

        print(
            f"Command     : {decision.command}"
        )

        print(
            f"Confidence  : {decision.confidence}"
        )

        print(
            "=================================\n"
        )

        return decision