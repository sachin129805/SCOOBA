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

    # ==================================================
    # TASK EXECUTION
    # ==================================================

    def execute_task(self, task):

        print(
            f"\n⚙ Executing Task: "
            f"{task.skill} -> "
            f"{task.action} "
            f"({task.entity})"
        )

        # ==================================================
        # BROWSER
        # ==================================================

        if task.skill == "browser":

            target = (
                task.entity
                or "google"
            ).lower().strip()

            # ---------------------------------------------
            # OPEN
            # ---------------------------------------------

            if task.action == "open":

                if target == "youtube":

                    print(
                        "▶ Opening YouTube..."
                    )

                    return self.browser.youtube()

                elif target == "google":

                    print(
                        "🌐 Opening Google..."
                    )

                    return self.browser.open_url(
                        "https://www.google.com"
                    )

                elif target == "github":

                    print(
                        "🐙 Opening GitHub..."
                    )

                    return self.browser.github()

                elif target == "gmail":

                    print(
                        "📧 Opening Gmail..."
                    )

                    return self.browser.gmail()

                elif target == "chatgpt":

                    print(
                        "🤖 Opening ChatGPT..."
                    )

                    return self.browser.chatgpt()

                print(
                    f"🖥 Opening application: "
                    f"{target}"
                )

                return self.desktop.open(
                    target
                )

            # ---------------------------------------------
            # SEARCH
            # ---------------------------------------------

            elif task.action == "search":

                if not task.query:

                    print(
                        "⚠ Browser search requires "
                        "a query."
                    )

                    return False

                if target == "youtube":

                    print(
                        f"🔎 YouTube Search: "
                        f"{task.query}"
                    )

                    return self.browser.youtube_search(
                        task.query
                    )

                elif target == "google":

                    print(
                        f"🔎 Google Search: "
                        f"{task.query}"
                    )

                    return self.browser.google_search(
                        task.query
                    )

                print(
                    f"🔎 Google Search: "
                    f"{task.query}"
                )

                return self.browser.google_search(
                    task.query
                )

            # ---------------------------------------------
            # PLAY FIRST YOUTUBE RESULT
            # ---------------------------------------------

            elif task.action == "play_first":

                if not task.query:

                    print(
                        "⚠ play_first requires "
                        "a query."
                    )

                    return False

                if target != "youtube":

                    print(
                        "⚠ play_first currently "
                        "supports YouTube only."
                    )

                    return False

                print(
                    f"▶ Playing first YouTube "
                    f"result: {task.query}"
                )

                return self.browser.play_first(
                    task.query
                )

            # ---------------------------------------------
            # UNKNOWN BROWSER ACTION
            # ---------------------------------------------

            print(
                f"⚠ Unknown browser action: "
                f"{task.action}"
            )

            return False

        # ==================================================
        # FILESYSTEM
        # ==================================================

        if task.skill == "filesystem":

            # ---------------------------------------------
            # CREATE FOLDER
            # ---------------------------------------------

            if task.action == "create_folder":

                if not task.entity:

                    print(
                        "⚠ Folder name missing."
                    )

                    return False

                return self.filesystem.create_folder(
                    task.entity
                )

            # ---------------------------------------------
            # CREATE FILE
            # ---------------------------------------------

            elif task.action == "create_file":

                if not task.entity:

                    print(
                        "⚠ File name missing."
                    )

                    return False

                return self.filesystem.create_file(
                    task.entity
                )

            print(
                f"⚠ Unknown filesystem action: "
                f"{task.action}"
            )

            return False

        # ==================================================
        # DEVELOPER
        # ==================================================

        if task.skill == "developer":

            print(
                f"⚠ Developer task not yet "
                f"connected: {task.action}"
            )

            return False

        # ==================================================
        # UNKNOWN SKILL
        # ==================================================

        print(
            f"⚠ Unknown skill: "
            f"{task.skill}"
        )

        return False

    # ==================================================
    # LEGACY DECISION EXECUTION
    # ==================================================

    def execute(self, decision):

        print(
            "\n========== LEGACY DECISION =========="
        )

        print(
            f"Intent      : "
            f"{decision.intent}"
        )

        print(
            f"Entity      : "
            f"{decision.entity}"
        )

        print(
            f"Action      : "
            f"{decision.action}"
        )

        print(
            f"Query       : "
            f"{decision.query}"
        )

        print(
            f"Target      : "
            f"{decision.target}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "=====================================\n"
        )

        if decision.intent is None:

            return False

        # ---------------------------------------------
        # SEARCH
        # ---------------------------------------------

        if decision.intent == "SEARCH":

            query = decision.query

            if not query:

                print(
                    "⚠ No search query detected."
                )

                return False

            target = (
                decision.target
                or decision.entity
                or "google"
            )

            target = target.lower().strip()

            if target == "youtube":

                print(
                    f"🔎 YouTube Search: "
                    f"{query}"
                )

                return self.browser.youtube_search(
                    query
                )

            elif target == "google":

                print(
                    f"🔎 Google Search: "
                    f"{query}"
                )

                return self.browser.google_search(
                    query
                )

            return self.browser.google_search(
                query
            )

        # ---------------------------------------------
        # OPEN APP
        # ---------------------------------------------

        if decision.intent == "OPEN_APP":

            if decision.entity is None:

                print(
                    "⚠ No application detected."
                )

                return False

            entity = (
                decision.entity
                .lower()
                .strip()
            )

            if entity == "youtube":

                return self.browser.youtube()

            elif entity == "google":

                return self.browser.open_url(
                    "https://www.google.com"
                )

            elif entity == "github":

                return self.browser.github()

            elif entity == "gmail":

                return self.browser.gmail()

            elif entity == "chatgpt":

                return self.browser.chatgpt()

            return self.desktop.open(
                entity
            )

        # ---------------------------------------------
        # CREATE FOLDER
        # ---------------------------------------------

        elif decision.intent == "CREATE_FOLDER":

            folder_name = (
                decision.target
                or decision.entity
            )

            if not folder_name:

                return False

            return self.filesystem.create_folder(
                folder_name
            )

        # ---------------------------------------------
        # CREATE FILE
        # ---------------------------------------------

        elif decision.intent == "CREATE_FILE":

            file_name = (
                decision.target
                or decision.entity
            )

            if not file_name:

                return False

            return self.filesystem.create_file(
                file_name
            )

        # ---------------------------------------------
        # CREATE PYTHON PROJECT
        # ---------------------------------------------

        elif decision.intent == (
            "CREATE_PYTHON_PROJECT"
        ):

            project_name = (
                decision.target
                or decision.entity
            )

            if not project_name:

                return False

            print(
                f"🐍 Creating Python project: "
                f"{project_name}"
            )

            return True

        # ---------------------------------------------
        # CLOSE APP
        # ---------------------------------------------

        elif decision.intent == "CLOSE_APP":

            print(
                "🛑 Close command detected."
            )

            return True

        return False