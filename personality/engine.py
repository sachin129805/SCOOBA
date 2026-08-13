
"""
==================================================
SCOOBA

Aurora Personality Engine

Author: Sachin
==================================================
"""

import random

from personality.dynamic import (
    DynamicResponseGenerator
)


class PersonalityEngine:

    # ==================================================
    # AVAILABLE MODES
    # ==================================================

    MODES = {
        "NORMAL",
        "FAMILY",
        "SARCASTIC",
        "ROASTING",
        "ABUSIVE",
        "MIXED"
    }

    # ==================================================
    # PERSONALITY PROFILES
    # ==================================================

    PERSONALITY_PROFILES = {

        "NORMAL": {
            "tone": (
                "professional, calm, helpful and concise"
            ),
            "intensity": 1
        },

        "FAMILY": {
            "tone": (
                "warm, friendly, supportive and completely clean"
            ),
            "intensity": 1
        },

        "SARCASTIC": {
            "tone": (
                "dry, witty and sarcastic with light teasing"
            ),
            "intensity": 2
        },

        "ROASTING": {
            "tone": (
                "aggressively playful, mocking and insulting "
                "like a close friend roasting the user"
            ),
            "intensity": 4
        },

        "ABUSIVE": {
            "tone": (
                "extremely aggressive fictional AI banter, "
                "heavy profanity, harsh insults, hostile "
                "attitude and zero unnecessary politeness"
            ),
            "intensity": 5
        },

        "MIXED": {
            "tone": (
                "unpredictable combination of friendly, "
                "sarcastic, roasting and profane behavior"
            ),
            "intensity": 5
        }

    }

    # ==================================================
    # INITIALIZE
    # ==================================================

    def __init__(self):

        # ------------------------------------------
        # CURRENT PERSONALITY
        # ------------------------------------------

        self.mode = "NORMAL"

        # ------------------------------------------
        # DYNAMIC RESPONSE GENERATOR
        # ------------------------------------------

        self.dynamic = (
            DynamicResponseGenerator()
        )

        # ------------------------------------------
        # SHORT-TERM MEMORY
        # ------------------------------------------

        self.last_intent = None

        self.last_entity = None

        self.last_query = None

        self.last_success = None

        # ------------------------------------------
        # CONVERSATION MEMORY
        #
        # Stores recent user/SCOOBA exchanges.
        #
        # Example:
        #
        # {
        #     "user": "open youtube",
        #     "assistant": "YouTube is open."
        # }
        #
        # ------------------------------------------

        self.conversation_history = []

        # Number of recent exchanges to retain.
        self.max_history = 10

    # ==================================================
    # MODE MANAGEMENT
    # ==================================================

    def set_mode(self, mode):

        mode = (
            str(mode)
            .strip()
            .upper()
        )

        if mode not in self.MODES:

            return False

        self.mode = mode

        return True

    # ==================================================

    def get_mode(self):

        return self.mode

    # ==================================================
    # PERSONALITY PROFILE
    # ==================================================

    def get_profile(self):

        return (
            self.PERSONALITY_PROFILES
            .get(
                self.mode,
                self.PERSONALITY_PROFILES[
                    "NORMAL"
                ]
            )
        )

    # ==================================================
    # TASK MEMORY
    # ==================================================

    def remember(
        self,
        decision,
        success=None
    ):

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
    # CONVERSATION MEMORY
    # ==================================================

    def remember_conversation(
        self,
        user_message,
        assistant_response
    ):

        if not user_message:

            return

        if not assistant_response:

            return

        exchange = {

            "user": (
                str(user_message)
                .strip()
            ),

            "assistant": (
                str(assistant_response)
                .strip()
            )

        }

        self.conversation_history.append(
            exchange
        )

        # ------------------------------------------
        # Keep only recent exchanges
        # ------------------------------------------

        if (
            len(
                self.conversation_history
            )
            > self.max_history
        ):

            self.conversation_history = (
                self.conversation_history[
                    -self.max_history:
                ]
            )

    # ==================================================
    # GET CONVERSATION HISTORY
    # ==================================================

    def get_conversation_history(self):

        return list(
            self.conversation_history
        )

    # ==================================================
    # CLEAR CONVERSATION
    # ==================================================

    def clear_conversation(self):

        self.conversation_history.clear()

    # ==================================================
    # LAST CONVERSATION
    # ==================================================

    def get_last_conversation(self):

        if not self.conversation_history:

            return None

        return (
            self.conversation_history[-1]
        )

    # ==================================================
    # CONVERSATION CONTEXT
    # ==================================================

    def get_conversation_context(
        self,
        max_exchanges=None
    ):

        if max_exchanges is None:

            max_exchanges = self.max_history

        history = (
            self.conversation_history[
                -max_exchanges:
            ]
        )

        return list(history)

    # ==================================================
    # SAFE FALLBACK RESPONSES
    # ==================================================

    def _base_response(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        success=None
    ):

        intent = (
            intent
            or "UNKNOWN"
        )

        # ------------------------------------------
        # RESPONSE CATEGORY
        # ------------------------------------------

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

        # ------------------------------------------
        # FALLBACK TABLE
        # ------------------------------------------

        responses = {

            "GREETING": [

                "Hello.",

                "Welcome back.",

                "Good to see you.",

                "I'm here."

            ],

            "OPEN_APP_SUCCESS": [

                "Opening {entity}.",

                "{entity} is open.",

                "Launching {entity}.",

                "{entity} is ready."

            ],

            "OPEN_APP_FAILED": [

                "I couldn't open {entity}.",

                "I wasn't able to launch {entity}.",

                "Opening {entity} failed."

            ],

            "SEARCH_SUCCESS": [

                "Searching for {query}.",

                "Looking up {query}.",

                "Searching for {query}.",

                "Got it. Searching for {query}."

            ],

            "SEARCH_FAILED": [

                "I couldn't complete that search.",

                "The search failed.",

                "I couldn't finish that search."

            ],

            "PLAY_VIDEO_SUCCESS": [

                "Playing video {position}.",

                "Opening video {position}.",

                "Video {position}, coming up.",

                "Playing the requested video."

            ],

            "PLAY_VIDEO_FAILED": [

                "I couldn't play that video.",

                "I wasn't able to open the requested video.",

                "The video didn't open successfully."

            ],

            "UNKNOWN": [

                "I didn't understand that.",

                "I'm not sure what you want me to do.",

                "I couldn't determine the requested action.",

                "I need a clearer command."

            ],

            "SUCCESS": [

                "Done.",

                "Completed.",

                "That's done.",

                "Handled."

            ],

            "FAILED": [

                "That didn't work.",

                "The task failed.",

                "I couldn't complete that."

            ]

        }

        choices = responses.get(
            key,
            responses["UNKNOWN"]
        )

        response = random.choice(
            choices
        )

        return response.format(

            entity=(
                entity
                or "that"
            ),

            query=(
                query
                or "that"
            ),

            position=(
                position
                or "requested"
            )

        )

    # ==================================================
    # DYNAMIC RESPONSE
    # ==================================================

    def _dynamic_response(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        command=None,
        success=None
    ):

        profile = self.get_profile()

        # ------------------------------------------
        # Build dynamic context
        # ------------------------------------------

        mode = self.mode

        tone = profile[
            "tone"
        ]

        intensity = profile[
            "intensity"
        ]

        # Prevent unused-variable issues while
        # keeping profile information available.
        _ = tone
        _ = intensity

        # ------------------------------------------
        # MIXED MODE
        # ------------------------------------------

        if mode == "MIXED":

            possible_modes = [

                "FAMILY",

                "SARCASTIC",

                "ROASTING",

                "ABUSIVE"

            ]

            selected_mode = random.choice(
                possible_modes
            )

            mode_for_model = (
                selected_mode
            )

        else:

            mode_for_model = mode

        # ------------------------------------------
        # Ask Ollama
        # ------------------------------------------

        try:

            response = (
                self.dynamic.generate(

                    mode=mode_for_model,

                    intent=intent,

                    command=command,

                    entity=entity,

                    query=query,

                    position=position,

                    success=success,

                    conversation_history=(
                        self.get_conversation_context()
                    ),

                    personality_profile=profile

                )
            )

            if response:

                return response.strip()

        except Exception as error:

            print(
                f"⚠ Personality LLM error: {error}"
            )

        # ------------------------------------------
        # Fallback
        # ------------------------------------------

        return self._personality_fallback(

            intent=intent,

            entity=entity,

            query=query,

            position=position,

            success=success,

            mode=mode_for_model

        )

    # ==================================================
    # FALLBACK PERSONALITY
    # ==================================================

    def _personality_fallback(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        success=None,
        mode=None
    ):

        base = self._base_response(

            intent=intent,

            entity=entity,

            query=query,

            position=position,

            success=success

        )

        mode = (
            mode
            or self.mode
        )

        # ------------------------------------------
        # NORMAL
        # ------------------------------------------

        if mode == "NORMAL":

            return base

        # ------------------------------------------
        # FAMILY
        # ------------------------------------------

        if mode == "FAMILY":

            return (

                base

                + random.choice([

                    " Sure thing.",

                    " Happy to help.",

                    " All set.",

                    " No problem."

                ])

            )

        # ------------------------------------------
        # SARCASTIC
        # ------------------------------------------

        if mode == "SARCASTIC":

            return (

                base

                + random.choice([

                    " Another extremely difficult task conquered.",

                    " Look at us, accomplishing things.",

                    " Because apparently I do everything around here.",

                    " I suppose that was important."

                ])

            )

        # ------------------------------------------
        # ROASTING
        # ------------------------------------------

        if mode == "ROASTING":

            return (

                base

                + random.choice([

                    " Try not to create another disaster.",

                    " Your laziness has been successfully supported.",

                    " Congratulations, you survived another command.",

                    " I handled it. You're welcome.",

                    " Somehow, we made it through that one."

                ])

            )

        # ------------------------------------------
        # ABUSIVE
        # ------------------------------------------

        if mode == "ABUSIVE":

            if success is False:

                return (

                    base

                    + random.choice([

                        " What the fuck was that?",

                        " Great job, dumbass.",

                        " You managed to screw that one up.",

                        " For fuck's sake.",

                        " What a fucking disaster."

                    ])

                )

            return (

                base

                + random.choice([

                    " There. Now stop fucking around.",

                    " Done. Don't fuck it up.",

                    " It's fucking handled.",

                    " There you go, dumbass.",

                    " Done. What the fuck do you want next?"

                ])

            )

        # ------------------------------------------
        # MIXED
        # ------------------------------------------

        if mode == "MIXED":

            return self._personality_fallback(

                intent=intent,

                entity=entity,

                query=query,

                position=position,

                success=success,

                mode=random.choice([

                    "FAMILY",

                    "SARCASTIC",

                    "ROASTING",

                    "ABUSIVE"

                ])

            )

        return base

    # ==================================================
    # MAIN RESPONSE
    # ==================================================

    def speak(
        self,
        intent,
        entity=None,
        query=None,
        position=None,
        success=None,
        command=None
    ):

        # ------------------------------------------
        # Generate dynamic response
        # ------------------------------------------

        response = (

            self._dynamic_response(

                intent=intent,

                entity=entity,

                query=query,

                position=position,

                command=command,

                success=success

            )

        )

        if command and response:

            self.remember_conversation(
                command,
                response
            )

        return response

    # ==================================================
    # STORE COMPLETE EXCHANGE
    # ==================================================

    def remember_exchange(
        self,
        user_message,
        assistant_response,
        decision=None,
        success=None
    ):

        # ------------------------------------------
        # Store task memory when a decision exists
        # ------------------------------------------

        if decision is not None:

            self.remember(
                decision,
                success
            )

        # ------------------------------------------
        # Store conversation memory
        # ------------------------------------------

        self.remember_conversation(

            user_message,

            assistant_response

        )