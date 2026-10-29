# ==============================================================================
# Scene:      ReallyHardToSolve
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 160-174)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReallyHardToSolve.py ReallyHardToSolve -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReallyHardToSolve(Scene):
    def construct(self):
        words = OldTexText(
            "They're", "really\\\\",
            "freaking", "hard\\\\",
            "to", "solve\\\\",
        )
        words.set_height(6)

        self.wait()
        for word in words:
            wait_time = 0.05 * len(word)
            self.add(word)
            self.wait(wait_time)
        self.wait()
