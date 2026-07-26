"""
==================================================
SCOOBA

Brain Engine

Author: Sachin
==================================================
"""

from rapidfuzz import process

from brain.responses import get_response


class Brain:

    def __init__(self):

        self.training = {

            "greeting": [

                "hello",
                "hi",
                "hey",
                "good morning",
                "good evening"

            ],

            "how_are_you": [

                "how are you",
                "how are ya",
                "how are you doing",
                "how have you been",
                "how r u"

            ],

            "creator": [

                "who made you",
                "who built you",
                "who created you"

            ],

            "thanks": [

                "thank you",
                "thanks",
                "thanks a lot"

            ]

        }

        self.threshold = 70

    def process(self, text):

        text = text.lower().strip()

        best_intent = None
        best_score = 0

        for intent, phrases in self.training.items():

            match = process.extractOne(
                text,
                phrases
            )

            if match:

                phrase, score, _ = match

                if score > best_score:

                    best_score = score
                    best_intent = intent

        print(f"\n🧠 Intent : {best_intent}")
        print(f"🎯 Confidence : {best_score:.1f}%")

        if best_score < self.threshold:

            return get_response("unknown")

        return get_response(best_intent)