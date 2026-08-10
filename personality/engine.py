"""
==================================================
SCOOBA

Aurora Personality Engine

Author: Sachin
==================================================
"""

import random


class PersonalityEngine:

    MODES = {
        "NORMAL",
        "FAMILY",
        "SARCASTIC",
        "ROASTING",
        "ABUSIVE",
        "MIXED",
    }

    def __init__(self):

        # ------------------------------------------
        # CURRENT PERSONALITY
        # ------------------------------------------

        self.mode = "NORMAL"

        # ------------------------------------------
        # SHORT-TERM CONVERSATION MEMORY
        # ------------------------------------------

        self.last_intent = None
        self.last_entity = None
        self.last_query = None
        self.last_success = None

        # ------------------------------------------
        # SAFE BASE RESPONSES
        #
        # These are building material, not complete
        # personality responses.
        # ------------------------------------------

        self.base = {

            "GREETING": [
                "Hello.",
                "Welcome back.",
                "Good to see you.",
                "I'm here.",
            ],

            "OPEN_APP_SUCCESS": [
                "Opening {entity}.",
                "{entity} is opening.",
                "Launching {entity}.",
                "{entity} is ready.",
            ],

            "OPEN_APP_FAILED": [
                "I couldn't open {entity}.",
                "I wasn't able to launch {entity}.",
                "Opening {entity} failed.",
            ],

            "SEARCH_SUCCESS": [
                "Searching for {query}.",
                "Looking up {query}.",
                "Searching {query}.",
                "Got it. Searching for {query}.",
            ],

            "SEARCH_FAILED": [
                "I couldn't complete that search.",
                "The search didn't complete successfully.",
                "I couldn't finish that search.",
            ],

            "PLAY_VIDEO_SUCCESS": [
                "Playing video {position}.",
                "Opening video {position}.",
                "Video {position}, coming up.",
                "Playing the requested video.",
            ],

            "PLAY_VIDEO_FAILED": [
                "I couldn't play that video.",
                "I wasn't able to open the requested video.",
                "The video didn't open successfully.",
            ],

            "UNKNOWN": [
                "I didn't understand that.",
                "I'm not sure what you want me to do.",
                "I couldn't determine the requested action.",
                "I need a clearer command.",
            ],

            "SUCCESS": [
                "Done.",
                "Completed.",
                "That's done.",
                "Handled.",
            ],

            "FAILED": [
                "That didn't work.",
                "The task failed.",
                "I couldn't complete that.",
            ],
        }

    # ==================================================
    # MODE MANAGEMENT
    # ==================================================

    def set_mode(self, mode):

        mode = str(mode).strip().upper()

        if mode not in self.MODES:
            return False

        self.mode = mode

        return True

    def get_mode(self):

        return self.mode

    # ==================================================
    # MEMORY
    # ==================================================

    def remember(self, decision, success=None):

        self.last_intent = getattr(
            decision,
            "intent",
            None
        )

        self.last_entity = getattr(
            decision,
            "entity",
            None
        )

        self.last_query = getattr(
            decision,
            "query",
            None
        )

        self.last_success = success

    # ==================================================
    # BASE RESPONSE
    # ==================================================

    def _base_response(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        success=None
    ):

        intent = intent or "UNKNOWN"

        if success is None:

            key = intent

        elif intent == "OPEN_APP":

            key = (
                "OPEN_APP_SUCCESS"
                if success
                else "OPEN_APP_FAILED"
            )

        elif intent == "SEARCH":

            key = (
                "SEARCH_SUCCESS"
                if success
                else "SEARCH_FAILED"
            )

        elif intent == "PLAY_VIDEO":

            key = (
                "PLAY_VIDEO_SUCCESS"
                if success
                else "PLAY_VIDEO_FAILED"
            )

        else:

            key = (
                "SUCCESS"
                if success
                else "FAILED"
            )

        choices = self.base.get(
            key,
            self.base["UNKNOWN"]
        )

        response = random.choice(choices)

        response = response.format(
            entity=entity or "that",
            query=query or "that",
            position=position or "requested"
        )

        return response

    # ==================================================
    # PERSONALITY TRANSFORMATION
    # ==================================================

    def _apply_personality(self, response):

        mode = self.mode

        # ------------------------------------------
        # NORMAL
        # ------------------------------------------

        if mode == "NORMAL":
            return response

        # ------------------------------------------
        # FAMILY
        # ------------------------------------------

        if mode == "FAMILY":

            return self._family(response)

        # ------------------------------------------
        # SARCASTIC
        # ------------------------------------------

        if mode == "SARCASTIC":

            return self._sarcastic(response)

        # ------------------------------------------
        # ROASTING
        # ------------------------------------------

        if mode == "ROASTING":

            return self._roasting(response)

        # ------------------------------------------
        # ABUSIVE
        # ------------------------------------------

        if mode == "ABUSIVE":

            return self._abusive(response)

        # ------------------------------------------
        # MIXED
        # ------------------------------------------

        if mode == "MIXED":

            return self._mixed(response)

        return response

    # ==================================================
    # FAMILY
    # ==================================================

    def _family(self, response):

        additions = [
            " Sure thing.",
            " Happy to help.",
            " All set.",
            " No problem.",
        ]

        return response + random.choice(
            additions
        )

    # ==================================================
    # SARCASTIC
    # ==================================================

    def _sarcastic(self, response):

        additions = [
            " Because apparently I have to do everything around here.",
            " As requested by the world's busiest person.",
            " Another extremely difficult task conquered.",
            " Look at us, accomplishing things.",
            " I suppose that was important.",
        ]

        return response + random.choice(
            additions
        )

    # ==================================================
    # ROASTING
    # ==================================================

    def _roasting(self, response):

        additions = [
            " Try not to create another disaster.",
            " Your laziness has been successfully supported.",
            " Congratulations, you survived another command.",
            " I handled it. You're welcome.",
            " Somehow, we made it through that one.",
        ]

        return response + random.choice(
            additions
        )

    # ==================================================
    # ABUSIVE
    # ==================================================

    def _abusive(self, response):

        additions = [
            " Now stop making my life difficult.",
            " There. Happy now?",
            " Finally, something you managed to ask correctly.",
            " Done. Try not to screw it up.",
            " You're welcome, genius.",
        ]

        return response + random.choice(
            additions
        )

    # ==================================================
    # MIXED
    # ==================================================

    def _mixed(self, response):

        # Dynamically select a personality style
        # for each response.

        styles = [
            self._family,
            self._sarcastic,
            self._roasting,
            self._abusive,
        ]

        style = random.choice(styles)

        return style(response)

    # ==================================================
    # MAIN RESPONSE
    # ==================================================

    def speak(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        success=None
    ):

        response = self._base_response(
            intent=intent,
            entity=entity,
            query=query,
            position=position,
            success=success
        )

        response = self._apply_personality(
            response
        )

        return response