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

    "SEARCH": {
        "verbs": [
            "search",
            "find",
            "look for",
            "google"
        ],
        "description": "Search for information using a target service"
    },

    "CREATE_PYTHON_PROJECT": {
        "verbs": [
            "create",
            "make",
            "generate",
            "build"
        ],
        "description": "Create a new Python project"
    },

    "CREATE_FOLDER": {
        "verbs": [
            "create folder",
            "make folder"
        ],
        "description": "Create a new folder"
    },

    "CREATE_FILE": {
        "verbs": [
            "create file",
            "make file"
        ],
        "description": "Create a new file"
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