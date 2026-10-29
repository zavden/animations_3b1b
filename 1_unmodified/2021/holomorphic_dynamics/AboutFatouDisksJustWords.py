# ==============================================================================
# Scene:      AboutFatouDisksJustWords
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3049-3062)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AboutFatouDisksJustWords.py AboutFatouDisksJustWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AboutFatouDisksJustWords(Scene):
    def construct(self):
        words = OldTexText(
            "(Small enough) disks around points in the Fatou set...\\\\",
            "...eventually shrink to 0"
        )
        words.arrange(DOWN, aligned_edge=LEFT)
        words.to_corner(UL)
        words.set_stroke(BLACK, 6, background=True)

        self.play(FadeIn(words[0], lag_ratio=0.1))
        self.wait()
        self.play(FadeIn(words[1], lag_ratio=0.1))
        self.wait()
