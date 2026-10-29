# ==============================================================================
# Scene:      BeTheFirst
# Source:     videos/_2021/some1.py (lines 1204-1217)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BeTheFirst.py BeTheFirst -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BeTheFirst(Scene):
    def construct(self):
        circ = Circle(color=RED)
        circ.stretch(5, 0)
        circ.set_height(0.4)

        circ.to_edge(LEFT)
        words = Text("Be the first!")
        words.next_to(circ, RIGHT, aligned_edge=UP)
        words.set_color(RED)

        self.play(ShowCreation(circ))
        self.play(Write(words))
        self.wait()
