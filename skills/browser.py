"""
==================================================
SCOOBA

Browser Skill

Author: Sachin
==================================================
"""

import urllib.parse

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)


class BrowserSkill:

    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(self):

        self.playwright = None

        self.browser = None

        self.page = None

    # ==================================================
    # BROWSER SESSION
    # ==================================================

    def _ensure_browser(self):

        # --------------------------------------------------
        # Browser already running
        # --------------------------------------------------

        if (
            self.browser
            and self.browser.is_connected()
            and self.page
            and not self.page.is_closed()
        ):

            return True

        try:

            print(
                "🌐 Starting Chrome..."
            )

            self.playwright = (
                sync_playwright().start()
            )

            self.browser = (
                self.playwright.chromium.launch(
                    channel="chrome",
                    headless=False
                )
            )

            self.page = (
                self.browser.new_page(
                    viewport={
                        "width": 1280,
                        "height": 900
                    }
                )
            )

            print(
                "✅ Chrome ready."
            )

            return True

        except Exception as e:

            print(
                f"❌ Could not start Chrome: {e}"
            )

            self.playwright = None

            self.browser = None

            self.page = None

            return False

    # ==================================================
    # CLOSE BROWSER
    # ==================================================

    def close(self):

        try:

            if self.browser:

                self.browser.close()

        except Exception:
            pass

        try:

            if self.playwright:

                self.playwright.stop()

        except Exception:
            pass

        self.browser = None

        self.page = None

        self.playwright = None

        print(
            "🌐 Browser closed."
        )

        return True

    # ==================================================
    # BASIC BROWSER
    # ==================================================

    def open_url(self, url):

        if not url:

            return False

        if not self._ensure_browser():

            return False

        try:

            self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            print(
                f"🌐 Opened: {url}"
            )

            return True

        except PlaywrightTimeoutError:

            print(
                "⚠ Page loading timed out, "
                "but the browser may still "
                "have opened the page."
            )

            return True

        except Exception as e:

            print(
                f"❌ Browser error: {e}"
            )

            return False

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

        if not query:

            print(
                "⚠ Google search requires "
                "a query."
            )

            return False

        encoded_query = urllib.parse.quote(
            query
        )

        url = (
            "https://www.google.com/search?q="
            f"{encoded_query}"
        )

        print(
            f"🔎 Google Search: {query}"
        )

        return self.open_url(
            url
        )

    # ==================================================
    # YOUTUBE SEARCH
    # ==================================================

    def youtube_search(self, query):

        if not query:

            print(
                "⚠ YouTube search requires "
                "a query."
            )

            return False

        encoded_query = urllib.parse.quote(
            query
        )

        url = (
            "https://www.youtube.com/results"
            f"?search_query={encoded_query}"
        )

        print(
            f"🔎 YouTube Search: {query}"
        )

        return self.open_url(
            url
        )

    # ==================================================
    # PLAY FIRST
    # ==================================================

    def play_first(self, query):

        print(
            f"▶ Playing first YouTube result: "
            f"{query}"
        )

        return self.play_video(
            query,
            1
        )

    # ==================================================
    # PLAY SPECIFIC RESULT
    # ==================================================

    def play_video(
        self,
        query,
        position
    ):

        if not query:

            print(
                "⚠ play_video requires "
                "a search query."
            )

            return False

        if (
            not position
            or position < 1
        ):

            print(
                "⚠ Invalid video position."
            )

            return False

        # ==================================================
        # START / REUSE BROWSER
        # ==================================================

        if not self._ensure_browser():

            return False

        encoded_query = urllib.parse.quote(
            query
        )

        search_url = (
            "https://www.youtube.com/results"
            f"?search_query={encoded_query}"
        )

        print(
            f"▶ Searching YouTube: {query}"
        )

        print(
            f"🎯 Target result: #{position}"
        )

        try:

            # ==================================================
            # OPEN SEARCH
            # ==================================================

            print(
                "🌐 Opening YouTube search..."
            )

            self.page.goto(
                search_url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            # ==================================================
            # WAIT FOR INITIAL RESULTS
            # ==================================================

            print(
                "🔎 Waiting for YouTube results..."
            )

            results = self.page.locator(
                "a#video-title"
            )

            try:

                results.first.wait_for(
                    state="visible",
                    timeout=10000
                )

            except PlaywrightTimeoutError:

                print(
                    "⚠ Initial results "
                    "did not appear immediately."
                )

            # ==================================================
            # LOAD ENOUGH RESULTS
            # ==================================================

            max_scrolls = max(
                5,
                position
            )

            for scroll_number in range(
                max_scrolls
            ):

                count = results.count()

                print(
                    f"   Results currently loaded: "
                    f"{count}"
                )

                # ------------------------------------------
                # Enough results
                # ------------------------------------------

                if count >= position:

                    break

                # ------------------------------------------
                # Scroll
                # ------------------------------------------

                print(
                    f"   ↓ Loading more results "
                    f"({scroll_number + 1}/"
                    f"{max_scrolls})"
                )

                self.page.mouse.wheel(
                    0,
                    1400
                )

                self.page.wait_for_timeout(
                    1500
                )

            # ==================================================
            # FINAL RESULT COUNT
            # ==================================================

            count = results.count()

            print(
                f"🎬 Results detected: {count}"
            )

            # ==================================================
            # RESULT NOT FOUND
            # ==================================================

            if count < position:

                print(
                    f"❌ Only {count} results "
                    f"found; result #{position} "
                    f"does not exist."
                )

                return False

            # ==================================================
            # SELECT RESULT
            # ==================================================

            selected = results.nth(
                position - 1
            )

            # ==================================================
            # SCROLL TO RESULT
            # ==================================================

            try:

                selected.scroll_into_view_if_needed()

            except Exception:

                pass

            self.page.wait_for_timeout(
                500
            )

            # ==================================================
            # GET TITLE
            # ==================================================

            title = (
                selected.get_attribute(
                    "title"
                )
            )

            if not title:

                try:

                    title = (
                        selected.inner_text()
                    )

                except Exception:

                    title = (
                        f"YouTube result #{position}"
                    )

            print(
                f"🎬 Result #{position}: "
                f"{title}"
            )

            # ==================================================
            # OPEN RESULT
            # ==================================================

            print(
                f"▶ Opening result #{position}..."
            )

            selected.click()

            # ==================================================
            # WAIT FOR VIDEO PAGE
            # ==================================================

            try:

                self.page.wait_for_url(
                    "**/watch**",
                    timeout=15000
                )

            except PlaywrightTimeoutError:

                print(
                    "⚠ Video page navigation "
                    "was not detected immediately."
                )

            # ==================================================
            # GIVE YOUTUBE TIME TO START
            # ==================================================

            self.page.wait_for_timeout(
                2000
            )

            # ==================================================
            # FINAL STATUS
            # ==================================================

            print(
                f"✅ YouTube result "
                f"#{position} opened."
            )

            print(
                "🎬 Video is now playing."
            )

            # ==================================================
            # IMPORTANT
            # ==================================================
            #
            # DO NOT:
            #
            # input(...)
            #
            # DO NOT:
            #
            # browser.close()
            #
            # The browser remains alive so SCOOBA
            # can continue using it.
            #
            # ==================================================

            return True

        except PlaywrightTimeoutError:

            print(
                "❌ Timed out while waiting "
                "for YouTube."
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

    # ==================================================
    # DESTRUCTOR
    # ==================================================

    def __del__(self):

        try:

            self.close()

        except Exception:

            pass