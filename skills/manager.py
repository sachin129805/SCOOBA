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

            # ==================================================
            # OPEN
            # ==================================================

            if task.action == "open":

                # ------------------------------------------
                # YOUTUBE
                # ------------------------------------------

                if target == "youtube":

                    print(
                        "▶ Opening YouTube..."
                    )

                    return self.browser.youtube()

                # ------------------------------------------
                # GOOGLE
                # ------------------------------------------

                elif target == "google":

                    print(
                        "🌐 Opening Google..."
                    )

                    return self.browser.google()

                # ------------------------------------------
                # GMAIL
                # ------------------------------------------

                elif target == "gmail":

                    print(
                        "📧 Opening Gmail..."
                    )

                    return self.browser.gmail()

                # ------------------------------------------
                # CHATGPT
                # ------------------------------------------

                elif target == "chatgpt":

                    print(
                        "🤖 Opening ChatGPT..."
                    )

                    return self.browser.chatgpt()

                # ------------------------------------------
                # GENERIC DESKTOP APP
                # ------------------------------------------

                return self.desktop.open(
                    target
                )

            # ==================================================
            # SEARCH
            # ==================================================

            elif task.action == "search":

                if not task.query:

                    print(
                        "⚠ Browser search requires "
                        "a query."
                    )

                    return False

                # ------------------------------------------
                # YOUTUBE
                # ------------------------------------------

                if target == "youtube":

                    print(
                        f"🔎 YouTube Search: "
                        f"{task.query}"
                    )

                    return self.browser.youtube_search(
                        task.query
                    )

                # ------------------------------------------
                # GOOGLE
                # ------------------------------------------

                elif target == "google":

                    print(
                        f"🔎 Google Search: "
                        f"{task.query}"
                    )

                    return self.browser.google_search(
                        task.query
                    )

                # ------------------------------------------
                # DEFAULT SEARCH
                # ------------------------------------------

                print(
                    f"🔎 Google Search: "
                    f"{task.query}"
                )

                return self.browser.google_search(
                    task.query
                )

            # ==================================================
            # PLAY FIRST
            # ==================================================

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

            # ==================================================
            # PLAY SPECIFIC RESULT
            # ==================================================

            elif task.action == "play_video":

                if not task.query:

                    print(
                        "⚠ play_video requires "
                        "a query."
                    )

                    return False

                if not task.position:

                    print(
                        "⚠ play_video requires "
                        "a result position."
                    )

                    return False

                if target != "youtube":

                    print(
                        "⚠ play_video currently "
                        "supports YouTube only."
                    )

                    return False

                print(
                    f"▶ Playing YouTube "
                    f"result #{task.position}: "
                    f"{task.query}"
                )

                return self.browser.play_video(
                    task.query,
                    task.position
                )

            # ==================================================
            # UNKNOWN BROWSER ACTION
            # ==================================================

            print(
                f"⚠ Unknown browser action: "
                f"{task.action}"
            )

            return False

        # ==================================================
        # FILESYSTEM
        # ==================================================

        if task.skill == "filesystem":

            if task.action == "create_folder":

                if not task.entity:

                    return False

                return self.filesystem.create_folder(
                    task.entity
                )

            elif task.action == "create_file":

                if not task.entity:

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
            "\n========== DECISION =========="
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
            f"Position    : "
            f"{decision.position}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "==============================\n"
        )

        # ==================================================
        # SEARCH
        # ==================================================

        if decision.intent == "SEARCH":

            if not decision.query:

                return False

            target = (
                decision.target
                or decision.entity
                or "google"
            )

            target = (
                target
                .lower()
                .strip()
            )

            if target == "youtube":

                return self.browser.youtube_search(
                    decision.query
                )

            return self.browser.google_search(
                decision.query
            )

        # ==================================================
        # PLAY VIDEO
        # ==================================================

        if decision.intent == "PLAY_VIDEO":

            query = decision.query

            position = (
                decision.position
                or 1
            )

            if not query:

                return False

            return self.browser.play_video(
                query,
                position
            )

        # ==================================================
        # OPEN APP
        # ==================================================

        if decision.intent == "OPEN_APP":

            if not decision.entity:

                return False

            entity = (
                decision.entity
                .lower()
                .strip()
            )

            if entity == "youtube":

                return self.browser.youtube()

            elif entity == "google":

                return self.browser.google()

            elif entity == "github":

                return self.browser.github()

            elif entity == "gmail":

                return self.browser.gmail()

            elif entity == "chatgpt":

                return self.browser.chatgpt()

            return self.desktop.open(
                entity
            )

        # ==================================================
        # CREATE FOLDER
        # ==================================================

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

        # ==================================================
        # CREATE FILE
        # ==================================================

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

        # ==================================================
        # CREATE PYTHON PROJECT
        # ==================================================

        elif (
            decision.intent
            == "CREATE_PYTHON_PROJECT"
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

        # ==================================================
        # CLOSE
        # ==================================================

        elif decision.intent == "CLOSE_APP":

            print(
                "🛑 Close command detected."
            )

            return True

        return False