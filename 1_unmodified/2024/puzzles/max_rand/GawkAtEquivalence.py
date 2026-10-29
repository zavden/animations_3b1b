# ==============================================================================
# Scene:      GawkAtEquivalence
# Source:     videos/_2024/puzzles/max_rand.py (lines 222-241)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GawkAtEquivalence.py GawkAtEquivalence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GawkAtEquivalence(InteractiveScene):
    def construct(self):
        # Test
        expr = VGroup(
            Text("max(rand(), rand())"),
            Tex(R"\updownarrow", font_size=90),
            Text("sqrt(rand())"),
        )
        expr.arrange(DOWN)
        expr.to_edge(UP)
        randy = Randolph()
        randy.to_edge(DOWN)

        self.add(expr)
        self.play(randy.change("confused", expr))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("maybe", expr))
        self.play(Blink(randy))
        self.wait()
