# ==============================================================================
# Scene:      TrueTheoremWords
# Source:     videos/_2023/clt/wordy_scenes.py (lines 839-849)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TrueTheoremWords.py TrueTheoremWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TrueTheoremWords(InteractiveScene):
    def construct(self):
        words = "Actual rigorous\nno-jokes-this-time\nCentral Limit Theorem"
        text = Text(words)
        text.set_height(0.3 * FRAME_HEIGHT)
        text.to_edge(UP)

        for word in ["Actual", "rigorous", "no-","jokes-", "this-", "time", "Central", "Limit", "Theorem"]:
            self.add(text[word])
            self.wait(0.1 * len(word))
        self.wait()
