"""
==================================================
SCOOBA

Memory Parser

Author: Sachin
==================================================
"""


class MemoryParser:

    def parse(self, text: str):

        text = text.lower().strip()

        if not text.startswith("remember"):
            return None

        sentence = text.replace("remember", "", 1).strip()

        if " is " in sentence:

            key, value = sentence.split(" is ", 1)

            return {
                "key": key.strip(),
                "value": value.strip()
            }

        return None