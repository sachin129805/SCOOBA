"""
==================================================
SCOOBA

Responses

Author: Sachin
==================================================
"""

import random


RESPONSES = {

    "greeting": [

        "Hello Sachin!",
        "Welcome back, Sachin.",
        "Good to see you again."

    ],

    "how_are_you": [

        "I'm doing great.",
        "All systems are operational."

    ],

    "creator": [

        "I was built by Sachin.",
        "Sachin is my creator."

    ],

    "thanks": [

        "You're welcome.",
        "Always happy to help."

    ],

    "unknown": [

        "I don't know that yet.",
        "I'm still learning."

    ]
}


def get_response(intent: str):

    return random.choice(
        RESPONSES[intent]
    )