# ==============================================================================
# Scene:      NickyCaseMention
# Source:     videos/_2020/sir.py (lines 2929-2949)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NickyCaseMention.py NickyCaseMention -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NickyCaseMention(Scene):
    def construct(self):
        words = OldTexText(
            "Artwork by Nicky Case\\\\",
            "...who is awesome."
        )
        words.scale(1)
        words.to_edge(LEFT)
        arrow = Arrow(
            words.get_top(),
            words.get_top() + 2 * UR + RIGHT,
            path_arc=-90 * DEGREES,
        )
        self.play(
            Write(words[0]),
            ShowCreation(arrow),
            run_time=1,
        )
        self.wait(2)
        self.play(Write(words[1]), run_time=1)
        self.wait()
