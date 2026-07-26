"""
==================================================
SCOOBA

Smart Command Normalizer

Author: Sachin
==================================================
"""

import re
from rapidfuzz import process


class CommandNormalizer:

    def __init__(self):

        self.phrases = {

            "your job": "youtube",
            "you tube": "youtube",
            "git hub": "github",
            "what's app": "whatsapp",
            "whats app": "whatsapp",
            "visual studio code": "vscode",
            "vs code": "vscode",
            "google chrome": "chrome"

        }

        self.words = [

            "youtube",
            "github",
            "chrome",
            "calculator",
            "notepad",
            "paint",
            "vscode",
            "gmail",
            "chatgpt",
            "spotify",
            "whatsapp"

        ]

    def normalize(self, text):

        text = text.lower()

        # ---------- Phrase replacements ----------

        for wrong, correct in self.phrases.items():

            text = text.replace(wrong, correct)

        # ---------- Remove punctuation ----------

        text = re.sub(r"[^\w\s]", "", text)

        # ---------- Fuzzy word correction ----------

        corrected = []

        for word in text.split():

            match = process.extractOne(
                word,
                self.words,
                score_cutoff=85
            )

            if match:

                corrected.append(match[0])

            else:

                corrected.append(word)

        return " ".join(corrected)