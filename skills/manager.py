"""
==================================================
SCOOBA

Skill Manager

Author: Sachin
==================================================
"""

from skills.desktop import DesktopSkill
from skills.browser import BrowserSkill
from skills.filesystem import FileSystemSkill


class SkillManager:

    def __init__(self):

        self.desktop = DesktopSkill()

        self.browser = BrowserSkill()

        self.filesystem = FileSystemSkill()

    def execute(self, decision):

        print("\n========== DECISION ==========")

        print(
            f"Intent      : "
            f"{decision.intent}"
        )

        print(
            f"Entity      : "
            f"{decision.entity}"
        )

        print(
            f"Query       : "
            f"{decision.query}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "==============================\n"
        )

        if decision.intent is None:

            return False

        # --------------------------------------------------
        # OPEN APP
        # --------------------------------------------------

        if decision.intent == "OPEN_APP":

            if decision.entity is None:

                print(
                    "⚠ No application detected."
                )

                return False

            entity = decision.entity.lower().strip()

            # ---------------------------------------------
            # YouTube
            # ---------------------------------------------

            if entity == "youtube":

                if decision.query:

                    print(
                        f"🔎 YouTube Search: "
                        f"{decision.query}"
                    )

                    return self.browser.youtube_search(
                        decision.query
                    )

                print(
                    "▶ Opening YouTube..."
                )

                return self.browser.youtube()

            # ---------------------------------------------
            # Google
            # ---------------------------------------------

            elif entity == "google":

                if decision.query:

                    print(
                        f"🔎 Google Search: "
                        f"{decision.query}"
                    )

                    return self.browser.google_search(
                        decision.query
                    )

                return self.browser.open_url(
                    "https://www.google.com"
                )

            # ---------------------------------------------
            # GitHub
            # ---------------------------------------------

            elif entity == "github":

                return self.browser.github()

            # ---------------------------------------------
            # Gmail
            # ---------------------------------------------

            elif entity == "gmail":

                return self.browser.gmail()

            # ---------------------------------------------
            # ChatGPT
            # ---------------------------------------------

            elif entity == "chatgpt":

                return self.browser.chatgpt()

            # ---------------------------------------------
            # Desktop Application
            # ---------------------------------------------

            return self.desktop.open(
                entity
            )

        # --------------------------------------------------
        # CREATE FOLDER
        # --------------------------------------------------

        elif decision.intent == "CREATE_FOLDER":

            folder_name = (
                decision.target
                or decision.entity
            )

            if not folder_name:

                print(
                    "⚠ No folder name detected."
                )

                return False

            success = (
                self.filesystem.create_folder(
                    folder_name
                )
            )

            if success:

                print(
                    f"✅ Folder "
                    f"'{folder_name}' created."
                )

            else:

                print(
                    f"❌ Failed to create folder "
                    f"'{folder_name}'."
                )

            return success

        # --------------------------------------------------
        # CREATE FILE
        # --------------------------------------------------

        elif decision.intent == "CREATE_FILE":

            file_name = (
                decision.target
                or decision.entity
            )

            if not file_name:

                print(
                    "⚠ No file name detected."
                )

                return False

            success = (
                self.filesystem.create_file(
                    file_name
                )
            )

            if success:

                print(
                    f"✅ File "
                    f"'{file_name}' created."
                )

            else:

                print(
                    f"❌ Failed to create file "
                    f"'{file_name}'."
                )

            return success

        # --------------------------------------------------
        # CREATE PYTHON PROJECT
        # --------------------------------------------------

        elif decision.intent == (
            "CREATE_PYTHON_PROJECT"
        ):

            project_name = (
                decision.target
                or decision.entity
            )

            print(
                f"🐍 Creating Python project: "
                f"{project_name}"
            )

            # TODO:
            # self.developer.create_python_project(
            #     project_name
            # )

            return True

        # --------------------------------------------------
        # CLOSE APP
        # --------------------------------------------------

        elif decision.intent == "CLOSE_APP":

            print(
                "🛑 Close command detected."
            )

            return True

        return False