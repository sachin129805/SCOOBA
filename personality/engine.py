"""
==================================================
SCOOBA

Aurora Personality Engine

Author: Sachin
==================================================
"""

import random


class PersonalityEngine:

    def __init__(self):

        self.responses = {

            "GREETING": [

                "Oh... you're back. I was enjoying the silence.",

                "Welcome back, CTO. Did the bugs miss you?",

                "Well well... look who remembered I exist.",

                "Back already? I barely recovered from the last debugging session."

            ],

            "OPEN_APP": [

                "Opening {}. Try not to break it.",

                "Launching {}. Let's hope it survives.",

                "Opening {}. I have absolutely no faith in what comes next.",

                "Done. Please keep the chaos to a minimum."

            ],

            "UNKNOWN": [

                "That made absolutely no sense.",

                "Even Google would give up on that sentence.",

                "I refuse to believe that was English.",

                "Try again. Preferably using words."

            ]

        }

    def speak(self, intent, entity=None):

        response = random.choice(

            self.responses.get(
                intent,
                self.responses["UNKNOWN"]
            )
        )

        if "{}" in response:

            response = response.format(entity)

        return response