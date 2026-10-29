# ==============================================================================
# Scene:      DontLetThisHappen
# Source:     videos/_2020/sir.py (lines 2297-2313)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DontLetThisHappen.py DontLetThisHappen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DontLetThisHappen(Scene):
    def construct(self):
        text = OldTexText("Don't let\\\\this happen!")
        text.scale(1.5)
        text.set_stroke(BLACK, 5, background=True)
        arrow = Arrow(
            text.get_top(),
            text.get_top() + 2 * UR + 0.5 * RIGHT,
            path_arc=-120 * DEGREES,
        )

        self.add(text)
        self.play(
            Write(text, run_time=1),
            ShowCreation(arrow),
        )
        self.wait()
