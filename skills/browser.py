"""
==================================================
SCOOBA

Browser Skill

Author: Sachin
==================================================
"""

import webbrowser
import urllib.parse


class BrowserSkill:

    def open_url(self, url):

        webbrowser.open(url)

        return True

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

    def google_search(self, query):

        query = urllib.parse.quote(query)

        return self.open_url(
            f"https://www.google.com/search?q={query}"
        )

    def youtube_search(self, query):

        query = urllib.parse.quote(query)

        return self.open_url(
            f"https://www.youtube.com/results?search_query={query}"
        )