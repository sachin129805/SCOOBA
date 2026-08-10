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
        self.context = None
        self.page = None

    # ==================================================
    # ENSURE BROWSER
    # ==================================================

    def _ensure_browser(self):

        # --------------------------------------------------
        # Existing browser
        # --------------------------------------------------

        if (
            self.browser
            and self.browser.is_connected()
            and self.context
            and not self.context.is_closed()
        ):

            # Existing page still alive
            if (
                self.page
                and not self.page.is_closed()
            ):

                return True

            # Page was closed, create another one
            try:

                self.page = (
                    self.context.new_page()
                )

                return True

            except Exception:
                pass

        # ==================================================
        # START PLAYWRIGHT
        # ==================================================

        try:

            print(
                "🚀 Starting Chrome..."
            )

            # IMPORTANT:
            #
            # Keep the Playwright object alive
            # on self.
            #

            self.playwright = (
                sync_playwright().start()
            )

            # ==================================================
            # LAUNCH CHROME
            # ==================================================

            self.browser = (
                self.playwright.chromium.launch(
                    channel="chrome",
                    headless=False
                )
            )

            print(
                "✅ Chrome launched."
            )

            # ==================================================
            # CREATE CONTEXT
            # ==================================================

            self.context = (
                self.browser.new_context(
                    viewport={
                        "width": 1280,
                        "height": 900
                    }
                )
            )

            # ==================================================
            # CREATE PAGE
            # ==================================================

            self.page = (
                self.context.new_page()
            )

            print(
                "✅ Browser context ready."
            )

            return True

        except Exception as e:

            print(
                "❌ Failed to start browser:"
            )

            print(
                f"   {e}"
            )

            self._cleanup_browser()

            return False

    # ==================================================
    # CHECK PAGE
    # ==================================================

    def _ensure_page(self):

        if not self._ensure_browser():

            return False

        # --------------------------------------------------
        # Page exists and is alive
        # --------------------------------------------------

        if (
            self.page
            and not self.page.is_closed()
        ):

            return True

        # --------------------------------------------------
        # Recreate page
        # --------------------------------------------------

        try:

            self.page = (
                self.context.new_page()
            )

            return True

        except Exception as e:

            print(
                f"❌ Could not create page: {e}"
            )

            return False

    # ==================================================
    # OPEN URL
    # ==================================================

    def open_url(self, url):

        if not url:

            print(
                "⚠ No URL provided."
            )

            return False

        try:

            if not self._ensure_page():

                return False

            print(
                f"🌐 Opening: {url}"
            )

            # ==================================================
            # NAVIGATE
            # ==================================================

            self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            print(
                f"✅ Opened: {url}"
            )

            # ==================================================
            # IMPORTANT
            # ==================================================
            #
            # NO input()
            # NO browser.close()
            #
            # SCOOBA continues immediately.
            #

            return True

        except PlaywrightTimeoutError:

            print(
                "⚠ Page load timed out."
            )

            # The page may still have loaded.

            return True

        except Exception as e:

            print(
                "❌ Browser error:"
            )

            print(
                f"   {e}"
            )

            return False

    # ==================================================
    # GOOGLE
    # ==================================================

    def google(self):

        return self.open_url(
            "https://www.google.com"
        )

    # ==================================================
    # YOUTUBE
    # ==================================================

    def youtube(self):

        return self.open_url(
            "https://www.youtube.com"
        )

    # ==================================================
    # GITHUB
    # ==================================================

    def github(self):

        return self.open_url(
            "https://github.com"
        )

    # ==================================================
    # GMAIL
    # ==================================================

    def gmail(self):

        return self.open_url(
            "https://mail.google.com"
        )

    # ==================================================
    # CHATGPT
    # ==================================================

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
            f"🔎 Searching Google: {query}"
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
            f"🔎 Searching YouTube: {query}"
        )

        return self.open_url(
            url
        )

    # ==================================================
    # PLAY FIRST
    # ==================================================

    def play_first(self, query):

        return self.play_video(
            query,
            1
        )

    # ==================================================
    # PLAY SPECIFIC VIDEO
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
            # ENSURE PAGE
            # ==================================================

            if not self._ensure_page():

                return False

            page = self.page

            # ==================================================
            # OPEN SEARCH
            # ==================================================

            print(
                "🌐 Opening YouTube search..."
            )

            page.goto(
                search_url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            # ==================================================
            # WAIT
            # ==================================================

            print(
                "🔎 Waiting for YouTube results..."
            )

            page.wait_for_timeout(
                2000
            )

            # ==================================================
            # RESULTS
            # ==================================================

            results = page.locator(
                "a#video-title"
            )

            # ==================================================
            # LOAD MORE
            # ==================================================

            max_scrolls = max(
                5,
                position
            )

            previous_count = -1

            for scroll_number in range(
                max_scrolls
            ):

                count = results.count()

                print(
                    f"   Results currently loaded: "
                    f"{count}"
                )

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

                page.mouse.wheel(
                    0,
                    1400
                )

                page.wait_for_timeout(
                    1500
                )

                # ------------------------------------------
                # Stop excessive scrolling
                # ------------------------------------------

                if count == previous_count:

                    page.wait_for_timeout(
                        1000
                    )

                previous_count = count

            # ==================================================
            # FINAL COUNT
            # ==================================================

            count = results.count()

            print(
                f"🎬 Results detected: {count}"
            )

            if count < position:

                print(
                    f"❌ Only {count} results "
                    f"found; result #{position} "
                    f"does not exist."
                )

                return False

            # ==================================================
            # SELECT
            # ==================================================

            selected = results.nth(
                position - 1
            )

            selected.scroll_into_view_if_needed()

            page.wait_for_timeout(
                500
            )

            # ==================================================
            # TITLE
            # ==================================================

            title = selected.get_attribute(
                "title"
            )

            if not title:

                try:

                    title = selected.inner_text()

                except Exception:

                    title = (
                        f"YouTube result "
                        f"#{position}"
                    )

            print(
                f"🎬 Result #{position}: "
                f"{title}"
            )

            # ==================================================
            # CLICK
            # ==================================================

            print(
                f"▶ Opening result #{position}..."
            )

            selected.click()

            # ==================================================
            # WAIT FOR VIDEO
            # ==================================================

            try:

                page.wait_for_url(
                    "**/watch?**",
                    timeout=15000
                )

            except PlaywrightTimeoutError:

                print(
                    "⚠ Video page navigation "
                    "was not detected immediately."
                )

            print(
                f"✅ YouTube result "
                f"#{position} opened."
            )

            # IMPORTANT:
            #
            # DO NOT WAIT FOR ENTER.
            #
            # DO NOT CLOSE BROWSER.
            #

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
    # CLEANUP
    # ==================================================

    def _cleanup_browser(self):

        try:

            if (
                self.context
                and not self.context.is_closed()
            ):

                self.context.close()

        except Exception:
            pass

        try:

            if (
                self.browser
                and self.browser.is_connected()
            ):

                self.browser.close()

        except Exception:
            pass

        try:

            if self.playwright:

                self.playwright.stop()

        except Exception:
            pass

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None

    # ==================================================
    # EXPLICIT CLOSE
    # ==================================================

    def close(self):

        print(
            "🌐 Closing SCOOBA browser..."
        )

        self._cleanup_browser()

        print(
            "✅ Browser closed."
        )