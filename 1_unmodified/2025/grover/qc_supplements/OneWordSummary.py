# ==============================================================================
# Scene:      OneWordSummary
# Source:     videos/_2025/grover/qc_supplements.py (lines 1146-1170)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneWordSummary.py OneWordSummary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OneWordSummary(InteractiveScene):
    def construct(self):
        # Replace "Parallelism" with "Pythagoras"
        prompt = Text("Source of the speed-up", font_size=72)
        prompt.move_to(2 * UP)

        words = VGroup(
            Text("Parallelism").set_color(TEAL),
            Text("Pythagoras").set_color(YELLOW),
        )
        words.scale(2)
        words.next_to(prompt, DOWN, LARGE_BUFF)
        strike = Line(words[0].get_left(), words[0].get_right())
        strike.set_stroke(RED, 10)

        self.add(prompt)
        self.add(words[0])
        self.wait()
        self.play(ShowCreation(strike))
        self.play(
            FadeIn(words[1], 0.5 * DOWN),
            words[0].animate.scale(0.75).shift(2 * DOWN).set_opacity(0.25),
            strike.animate.scale(0.75).shift(2 * DOWN),
        )
        self.wait()
