"""
==================================================
SCOOBA

Skill Manager

Author: Sachin
==================================================
"""

from skills.desktop import DesktopSkill
from skills.browser import BrowserSkill


class SkillManager:

    def __init__(self):

        self.desktop = DesktopSkill()

        self.browser = BrowserSkill()

    def execute(self, decision):

        print("\n========== DECISION ==========")
        print(f"Intent      : {decision.intent}")
        print(f"Entity      : {decision.entity}")
        print(f"Confidence  : {decision.confidence}")
        print("==============================\n")

        if decision.intent != "OPEN_APP":

            return False

        if decision.entity is None:

            print("⚠ No application detected.")

            return False

        browser_apps = {

            "youtube": self.browser.youtube,
            "github": self.browser.github,
            "gmail": self.browser.gmail,
            "chatgpt": self.browser.chatgpt

        }

        if decision.entity in browser_apps:

            browser_apps[decision.entity]()

            return True

        return self.desktop.open(decision.entity)