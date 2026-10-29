# ==============================================================================
# Scene:      SimpleFEq
# Source:     videos/_2023/moser_reboot/main.py (lines 968-981)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleFEq.py SimpleFEq -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleFEq(InteractiveScene):
    def construct(self):
        F_eq = Tex("F = E - V + 2")
        F_eq.to_edge(UP)
        one = Tex("1")
        one.move_to(F_eq["2"], DOWN)

        self.add(F_eq)
        self.wait()
        self.play(
            FadeOut(F_eq["2"][0], 0.5 * UP),
            FadeIn(one, 0.5 * UP),
        )
        self.wait()
