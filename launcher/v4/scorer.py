"""
==================================================
SCOOBA V4

Application Scorer

Assigns a quality score to applications.

Author: Sachin
==================================================
"""


class ApplicationScorer:

    GOOD_WORDS = {

        "chrome",
        "brave",
        "edge",
        "firefox",
        "cursor",
        "code",
        "visual studio",
        "vscode",
        "docker",
        "steam",
        "blender",
        "krita",
        "vlc",
        "filmora",
        "github",
        "git",
        "mysql",
        "excel",
        "word",
        "powerpoint",
        "onenote",
        "notepad",
        "paint",
        "calculator",
        "terminal",
        "powershell",
        "cmd",
        "command prompt",
        "file explorer",
        "explorer",
        "copilot",
        "zoom",
        "pdfgear",
        "droidcam",
        "python",
        "pycharm",
        "node",
        "office"

    }

    BAD_WORDS = {

        "about",
        "offers",
        "documentation",
        "manual",
        "website",
        "sample",
        "samples",
        "example",
        "examples",
        "release notes",
        "readme",
        "tutorial",
        "update",
        "updater",
        "check for updates",
        "configure",
        "installer",
        "uninstall",
        "repair",
        "redistributable",
        "runtime",
        "console",
        "launcher prerequisites",
        "nativepush",
        "module search",
        "cpan",
        "java auto updater"

    }

    @classmethod
    def score(cls, name: str) -> int:

        name = name.lower()

        score = 50

        for word in cls.GOOD_WORDS:

            if word in name:
                score += 50

        for word in cls.BAD_WORDS:

            if word in name:
                score -= 100

        return score

    @classmethod
    def allowed(cls, name: str) -> bool:

        return cls.score(name) > 0