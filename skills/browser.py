"""
==================================================
SCOOBA

Browser Skill

Author: Sachin
==================================================
"""

import webbrowser
import urllib.parse

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)


class BrowserSkill:

    # ==================================================
    # BASIC BROWSER
    # ==================================================

    def open_url(self, url):

        webbrowser.open(url)

        return True

    # ==================================================
    # WEBSITES
    # ==================================================

    def youtube(self):

        return self.open_url(
            "https://www.youtube.com"
        )

    def github(self):

        return self.open_url(
            "https://github.com"
        )

    def gmail(self):

        return self.open_url(
            "https://mail.google.com"
        )

    def chatgpt(self):

        return self.open_url(
            "https://chat.openai.com"
        )

    # ==================================================
    # GOOGLE SEARCH
    # ==================================================

    def google_search(self, query):

        query = urllib.parse.quote(
            query
        )

        return self.open_url(
            "https://www.google.com/search?q="
            f"{query}"
        )

    # ==================================================
    # YOUTUBE SEARCH
    # ==================================================

    def youtube_search(self, query):

        query = urllib.parse.quote(
            query
        )

        return self.open_url(
            "https://www.youtube.com/results"
            f"?search_query={query}"
        )

    # ==================================================
    # YOUTUBE PLAY FIRST
    # ==================================================

    def play_first(self, query):

        if not query:

            print(
                "⚠ play_first requires "
                "a search query."
            )

            return False

        print(
            f"▶ Playing first YouTube result: "
            f"{query}"
        )

        search_url = (
            "https://www.youtube.com/results"
            "?search_query="
            + urllib.parse.quote(query)
        )

        try:

            with sync_playwright() as p:

                # ---------------------------------
                # Use installed Google Chrome
                # ---------------------------------

                browser = p.chromium.launch(
                    channel="chrome",
                    headless=False
                )

                page = browser.new_page()

                # ---------------------------------
                # Open YouTube Search
                # ---------------------------------

                print(
                    "🌐 Opening YouTube search..."
                )

                page.goto(
                    search_url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                # ---------------------------------
                # Wait for first result
                # ---------------------------------

                print(
                    "🔎 Waiting for YouTube results..."
                )

                first_result = page.locator(
                    "a#video-title"
                ).first

                first_result.wait_for(
                    state="visible",
                    timeout=15000
                )

                # ---------------------------------
                # Get title
                # ---------------------------------

                title = (
                    first_result
                    .get_attribute("title")
                )

                if title:

                    print(
                        f"🎬 First result: "
                        f"{title}"
                    )

                # ---------------------------------
                # Click first result
                # ---------------------------------

                print(
                    "▶ Opening first result..."
                )

                first_result.click()

                # ---------------------------------
                # Wait for video page
                # ---------------------------------

                page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=15000
                )

                print(
                    "✅ First YouTube result opened."
                )

                input(
                    "\nPress ENTER to close "
                    "the browser..."
                )

                browser.close()

                return True

        except PlaywrightTimeoutError:

            print(
                "❌ Timed out while finding "
                "the first YouTube result."
            )

            return False

        except Exception as e:

            print(
                "❌ YouTube automation failed:"
            )

            print(
                f"   {e}"
            )

            return False