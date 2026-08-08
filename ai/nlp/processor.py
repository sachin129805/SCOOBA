"""
==================================================
SCOOBA

NLP Processor

Author: Sachin
==================================================
"""

import spacy

from ai.intent.classifier import IntentClassifier


class NLPProcessor:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

        self.classifier = IntentClassifier()

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
            "lemmas": [],
            "tokens": []
        }

        # ---------------------------------
        # Extract Tokens & Lemmas
        # ---------------------------------

        for token in doc:

            result["tokens"].append(
                token.text
            )

            result["lemmas"].append(
                token.lemma_
            )

        # ---------------------------------
        # Intent Classification
        # ---------------------------------

        result["intent"] = self.classifier.classify(
            result["lemmas"]
        )

        # ---------------------------------
        # Browser Applications
        # ---------------------------------

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

        # ---------------------------------
        # PLAY VIDEO
        # ---------------------------------

        if result["intent"] == "PLAY_VIDEO":

            result["action"] = "play"

            # ---------------------------------
            # Determine YouTube
            # ---------------------------------

            result["entity"] = "youtube"
            result["target"] = "youtube"

            # ---------------------------------
            # Pattern:
            #
            # sb737 and play the first video
            # ---------------------------------

            if " and play " in text:

                query_part = text.split(
                    " and play ",
                    1
                )[0].strip()

                if query_part:

                    result["query"] = query_part

            # ---------------------------------
            # Pattern:
            #
            # play avicii the nights
            # ---------------------------------

            elif text.startswith("play "):

                query_part = text[
                    len("play "):
                ].strip()

                # Remove "the first video"
                # when explicitly present.

                suffixes = [
                    " and play the first video",
                    " play the first video",
                    " and play first video",
                    " play first video"
                ]

                for suffix in suffixes:

                    if query_part.endswith(
                        suffix
                    ):

                        query_part = (
                            query_part[
                                :-len(suffix)
                            ].strip()
                        )

                        break

                if query_part:

                    result["query"] = query_part

            # ---------------------------------
            # Pattern:
            #
            # watch avicii
            # ---------------------------------

            elif text.startswith("watch "):

                query_part = text[
                    len("watch "):
                ].strip()

                if query_part:

                    result["query"] = query_part

        # ---------------------------------
        # Browser Search Query
        # ---------------------------------

        elif result["intent"] == "SEARCH":

            query = None

            # ---------------------------------
            # search youtube for good day
            # ---------------------------------

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

            # ---------------------------------
            # find cats on youtube
            # ---------------------------------

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

            # ---------------------------------
            # look for cats on youtube
            # ---------------------------------

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

            # ---------------------------------
            # Clean Query
            # ---------------------------------

            if query:

                query = query.rstrip(
                    ".,!?;:"
                ).strip()

                result["query"] = query

            result["action"] = "search"

        # ---------------------------------
        # File / Folder / Project
        # ---------------------------------

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

        # ---------------------------------
        # Open App
        # ---------------------------------

        elif result["intent"] == "OPEN_APP":

            result["action"] = "open"

        # ---------------------------------
        # Close App
        # ---------------------------------

        elif result["intent"] == "CLOSE_APP":

            result["action"] = "close"

        # ---------------------------------
        # Debug
        # ---------------------------------

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
            "Intent :",
            result["intent"]
        )

        print(
            "Entity :",
            result["entity"]
        )

        print(
            "Query  :",
            result["query"]
        )

        print(
            "Target :",
            result["target"]
        )

        print(
            "Action :",
            result["action"]
        )

        print(
            "===============================\n"
        )

        return result