"""
==================================================
SCOOBA

NLP Processor

Author: Sachin
==================================================
"""

import re
import spacy

from ai.intent.classifier import IntentClassifier


class NLPProcessor:

    # ==================================================
    # NUMBER WORDS
    # ==================================================

    NUMBER_WORDS = {

        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10,
        "eleventh": 11,
        "twelfth": 12,
        "thirteenth": 13,
        "fourteenth": 14,
        "fifteenth": 15,
        "sixteenth": 16,
        "seventeenth": 17,
        "eighteenth": 18,
        "nineteenth": 19,
        "twentieth": 20
    }

    # ==================================================
    # VIDEO POSITION PHRASES
    # ==================================================

    POSITION_PATTERNS = [

        # the fourth video
        re.compile(
            r"\bthe\s+"
            r"(first|second|third|fourth|fifth|sixth|"
            r"seventh|eighth|ninth|tenth|eleventh|"
            r"twelfth|thirteenth|fourteenth|fifteenth|"
            r"sixteenth|seventeenth|eighteenth|"
            r"nineteenth|twentieth)"
            r"\s+(?:video|result)\b"
        ),

        # fourth video
        re.compile(
            r"\b"
            r"(first|second|third|fourth|fifth|sixth|"
            r"seventh|eighth|ninth|tenth|eleventh|"
            r"twelfth|thirteenth|fourteenth|fifteenth|"
            r"sixteenth|seventeenth|eighteenth|"
            r"nineteenth|twentieth)"
            r"\s+(?:video|result)\b"
        ),

        # 4th video / 4th result
        re.compile(
            r"\b(\d+)(?:st|nd|rd|th)"
            r"\s+(?:video|result)\b"
        ),

        # video number 4
        re.compile(
            r"\b(?:video|result)"
            r"\s+(?:number|no\.?)\s*(\d+)\b"
        ),

        # number 4
        re.compile(
            r"\bnumber\s+(\d+)\b"
        ),

        # result #4
        re.compile(
            r"\b(?:result|video)\s*#\s*(\d+)\b"
        ),

        # result 4
        re.compile(
            r"\b(?:result|video)\s+(\d+)\b"
        )
    ]

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

        self.classifier = IntentClassifier()

    # ==================================================
    # EXTRACT VIDEO POSITION
    # ==================================================

    def extract_position(self, text):

        # --------------------------------------------------
        # Word-based positions
        # --------------------------------------------------

        for pattern in self.POSITION_PATTERNS:

            match = pattern.search(text)

            if not match:
                continue

            value = match.group(1)

            if value.isdigit():

                return int(value)

            if value in self.NUMBER_WORDS:

                return self.NUMBER_WORDS[value]

        return None

    # ==================================================
    # REMOVE POSITION PHRASE
    # ==================================================

    def remove_position_phrase(self, text):

        cleaned = text

        # --------------------------------------------------
        # Remove phrases such as:
        #
        # the fourth video
        # fourth video
        # 4th video
        # fourth result
        # result number 4
        # number 4
        # --------------------------------------------------

        patterns = [

            r"\bthe\s+"
            r"(?:first|second|third|fourth|fifth|sixth|"
            r"seventh|eighth|ninth|tenth|eleventh|"
            r"twelfth|thirteenth|fourteenth|fifteenth|"
            r"sixteenth|seventeenth|eighteenth|"
            r"nineteenth|twentieth)"
            r"\s+(?:video|result)\b",

            r"\b"
            r"(?:first|second|third|fourth|fifth|sixth|"
            r"seventh|eighth|ninth|tenth|eleventh|"
            r"twelfth|thirteenth|fourteenth|fifteenth|"
            r"sixteenth|seventeenth|eighteenth|"
            r"nineteenth|twentieth)"
            r"\s+(?:video|result)\b",

            r"\b\d+(?:st|nd|rd|th)"
            r"\s+(?:video|result)\b",

            r"\b(?:video|result)"
            r"\s+(?:number|no\.?)\s*\d+\b",

            r"\bnumber\s+\d+\b",

            r"\b(?:result|video)"
            r"\s*#\s*\d+\b",

            r"\b(?:result|video)"
            r"\s+\d+\b"
        ]

        for pattern in patterns:

            cleaned = re.sub(
                pattern,
                "",
                cleaned,
                flags=re.IGNORECASE
            )

        return cleaned.strip()

    # ==================================================
    # CLEAN QUERY
    # ==================================================

    def clean_query(self, query):

        if not query:

            return None

        query = query.strip()

        # Remove command leftovers
        query = re.sub(
            r"^\s*(?:the\s+)?(?:video|result)\s+(?:of|for)\s+",
            "",
            query,
            flags=re.IGNORECASE
        )

        query = re.sub(
            r"^\s*(?:of|for)\s+",
            "",
            query,
            flags=re.IGNORECASE
        )

        query = query.strip()

        query = query.rstrip(
            ".,!?;:"
        ).strip()

        return query or None

    # ==================================================
    # EXTRACT PLAY QUERY
    # ==================================================

    def extract_play_query(
        self,
        text,
        position
    ):

        working = text

        # --------------------------------------------------
        # Remove position phrase first
        # --------------------------------------------------

        working = self.remove_position_phrase(
            working
        )

        # --------------------------------------------------
        # Patterns
        #
        # play avicii
        # play the fourth video of avicii
        # play the fourth video for avicii
        # avicii and play the fourth video
        # watch alan walker faded
        # --------------------------------------------------

        patterns = [

            # ----------------------------------------------
            # "... and play ..."
            # ----------------------------------------------

            r"^(.*?)\s+and\s+play\b",

            # ----------------------------------------------
            # "... and watch ..."
            # ----------------------------------------------

            r"^(.*?)\s+and\s+watch\b",

            # ----------------------------------------------
            # "play ..."
            # ----------------------------------------------

            r"^\s*play\b",

            # ----------------------------------------------
            # "watch ..."
            # ----------------------------------------------

            r"^\s*watch\b"
        ]

        # --------------------------------------------------
        # Special case:
        #
        # "play the fourth video of michael jackson"
        #
        # After removing position:
        #
        # "play of michael jackson"
        #
        # --------------------------------------------------

        if re.match(
            r"^\s*(?:play|watch)\b",
            working
        ):

            working = re.sub(
                r"^\s*(?:play|watch)\b",
                "",
                working,
                count=1
            ).strip()

            working = re.sub(
                r"^\s+(?:the\s+)?(?:video|result)"
                r"\s+(?:of|for)\s+",
                "",
                working,
                flags=re.IGNORECASE
            ).strip()

            working = re.sub(
                r"^\s+(?:of|for)\s+",
                "",
                working,
                flags=re.IGNORECASE
            ).strip()

            return self.clean_query(
                working
            )

        # --------------------------------------------------
        # "michael jackson and play..."
        # --------------------------------------------------

        match = re.match(
            r"^(.*?)\s+and\s+(?:play|watch)\b",
            working
        )

        if match:

            query = match.group(1).strip()

            return self.clean_query(
                query
            )

        return self.clean_query(
            working
        )

    # ==================================================
    # PROCESS
    # ==================================================

    def process(self, text: str):

        text = text.lower().strip()

        doc = self.nlp(text)

        result = {

            "intent": None,

            "entity": None,

            "query": None,

            "target": None,

            "action": None,

            "location": None,

            "position": None,

            "lemmas": [],

            "tokens": []
        }

        # ==================================================
        # TOKENS + LEMMAS
        # ==================================================

        for token in doc:

            result["tokens"].append(
                token.text
            )

            result["lemmas"].append(
                token.lemma_
            )

        # ==================================================
        # CLASSIFY INTENT
        # ==================================================

        result["intent"] = (
            self.classifier.classify(
                result["lemmas"]
            )
        )

        # ==================================================
        # BROWSER SITES
        # ==================================================

        browser_sites = [

            "youtube",
            "github",
            "gmail",
            "chatgpt",
            "google"
        ]

        for site in browser_sites:

            if site in text:

                result["entity"] = site

                result["target"] = site

                break

        # ==================================================
        # PLAY VIDEO
        # ==================================================

        if result["intent"] == "PLAY_VIDEO":

            result["action"] = "play"

            # --------------------------------------------------
            # PLAY VIDEO IS CURRENTLY YOUTUBE
            # --------------------------------------------------

            result["entity"] = "youtube"

            result["target"] = "youtube"

            # --------------------------------------------------
            # Position
            # --------------------------------------------------

            result["position"] = (
                self.extract_position(text)
            )

            # --------------------------------------------------
            # Query
            # --------------------------------------------------

            result["query"] = (
                self.extract_play_query(
                    text,
                    result["position"]
                )
            )

            # --------------------------------------------------
            # Default to first result if no
            # position was specified.
            # --------------------------------------------------

            if result["position"] is None:

                result["position"] = 1

        # ==================================================
        # SEARCH
        # ==================================================

        elif result["intent"] == "SEARCH":

            query = None

            # --------------------------------------------------
            # search youtube for good day
            # --------------------------------------------------

            if "search " in text:

                search_part = text.split(
                    "search ",
                    1
                )[1].strip()

                if " for " in search_part:

                    target_part, query_part = (
                        search_part.split(
                            " for ",
                            1
                        )
                    )

                    target_part = (
                        target_part.strip()
                    )

                    query_part = (
                        query_part.strip()
                    )

                    if target_part in browser_sites:

                        result["entity"] = (
                            target_part
                        )

                        result["target"] = (
                            target_part
                        )

                        query = query_part

                    else:

                        query = search_part

                else:

                    query = search_part

            # --------------------------------------------------
            # find cats on youtube
            # --------------------------------------------------

            elif "find " in text:

                find_part = text.split(
                    "find ",
                    1
                )[1].strip()

                for site in browser_sites:

                    suffix = (
                        " on " + site
                    )

                    if find_part.endswith(
                        suffix
                    ):

                        query = (
                            find_part[
                                :-len(suffix)
                            ].strip()
                        )

                        result["entity"] = site

                        result["target"] = site

                        break

                if query is None:

                    query = find_part

            # --------------------------------------------------
            # look for cats on youtube
            # --------------------------------------------------

            elif "look for " in text:

                look_part = text.split(
                    "look for ",
                    1
                )[1].strip()

                for site in browser_sites:

                    suffix = (
                        " on " + site
                    )

                    if look_part.endswith(
                        suffix
                    ):

                        query = (
                            look_part[
                                :-len(suffix)
                            ].strip()
                        )

                        result["entity"] = site

                        result["target"] = site

                        break

                if query is None:

                    query = look_part

            if query:

                query = query.rstrip(
                    ".,!?;:"
                ).strip()

                result["query"] = query

            result["action"] = "search"

        # ==================================================
        # CREATE FILE / FOLDER / PROJECT
        # ==================================================

        if result["intent"] in (

            "CREATE_PYTHON_PROJECT",
            "CREATE_FOLDER",
            "CREATE_FILE"
        ):

            keywords = [

                "called",
                "named",
                "project",
                "folder",
                "file"
            ]

            for keyword in keywords:

                if keyword in text:

                    entity = text.split(
                        keyword,
                        1
                    )[1].strip()

                    entity = entity.rstrip(
                        ".,!?;:"
                    ).strip()

                    if entity:

                        result["entity"] = entity

                        result["target"] = entity

                        break

            result["action"] = "create"

        # ==================================================
        # OPEN APP
        # ==================================================

        elif result["intent"] == "OPEN_APP":

            result["action"] = "open"

        # ==================================================
        # CLOSE APP
        # ==================================================

        elif result["intent"] == "CLOSE_APP":

            result["action"] = "close"

        # ==================================================
        # DEBUG
        # ==================================================

        print(
            "\n========== NLP DEBUG =========="
        )

        for token in doc:

            print(
                f"{token.text:<15}"
                f"POS={token.pos_:<10}"
                f"Lemma={token.lemma_}"
            )

        print("--------------------------------")

        print(
            "Intent   :",
            result["intent"]
        )

        print(
            "Entity   :",
            result["entity"]
        )

        print(
            "Query    :",
            result["query"]
        )

        print(
            "Target   :",
            result["target"]
        )

        print(
            "Action   :",
            result["action"]
        )

        print(
            "Position :",
            result["position"]
        )

        print(
            "===============================\n"
        )

        return result