# ==============================================================================
# Scene:      LookAtRemainderMod710
# Source:     videos/_2019/spirals.py (lines 3352-3387)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookAtRemainderMod710.py LookAtRemainderMod710 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LookAtRemainderMod710(Scene):
    def construct(self):
        t2c = {
            "n": YELLOW,
            "r": GREEN
        }
        equation = OldTex(
            "n", "=", "710", "k", "+", "r",
            tex_to_color_map=t2c,
        )
        equation.scale(1.5)

        n_arrow = Vector(UP).next_to(equation.get_part_by_tex("n"), DOWN)
        r_arrow = Vector(UP).next_to(equation.get_part_by_tex("r"), DOWN)
        n_arrow.set_color(t2c["n"])
        r_arrow.set_color(t2c["r"])

        n_label = OldTexText("Some\\\\number")
        r_label = OldTexText("Remainder")
        VGroup(n_label, r_label).scale(1.5)
        n_label.next_to(n_arrow, DOWN)
        n_label.match_color(n_arrow)
        r_label.next_to(r_arrow, DOWN)
        r_label.match_color(r_arrow)

        self.add(equation)
        self.play(
            FadeIn(n_label, UP),
            ShowCreation(n_arrow),
        )
        self.wait()
        self.play(
            FadeIn(r_label, DOWN),
            ShowCreation(r_arrow),
        )
        self.wait()
