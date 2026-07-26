"""
==================================================
SCOOBA

Intent Registry

Author: Sachin
==================================================
"""

INTENTS = {

    "OPEN_APP": {
        "verbs": [
            "open",
            "launch",
            "start",
            "run"
        ],
        "description": "Launch an installed application"
    },

    "CLOSE_APP": {
        "verbs": [
            "close",
            "exit",
            "quit",
            "terminate"
        ],
        "description": "Close a running application"
    },

    "GREETING": {
        "verbs": [
            "hello",
            "hi",
            "hey"
        ],
        "description": "Greeting the assistant"
    }

}