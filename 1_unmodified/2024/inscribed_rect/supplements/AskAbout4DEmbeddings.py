# ==============================================================================
# Scene:      AskAbout4DEmbeddings
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 579-624)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl AskAbout4DEmbeddings.py AskAbout4DEmbeddings -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/inscribed_rect/helpers.py -----

def mobius_strip_func(u, v, outer_radius=1.5, inner_radius=0.5):
    theta = TAU * v
    phi = theta / 2
    p = math.cos(theta) * RIGHT + math.sin(theta) * UP
    q = math.cos(phi) * p + math.sin(phi) * OUT
    return outer_radius * p + inner_radius * q * (2 * u - 1)



# ----- From _2024/inscribed_rect/supplements.py -----

class AskAbout4DEmbeddings(TeacherStudentsScene):
    def construct(self):
        # Hold up terms
        morty = self.teacher
        stds = self.students
        randy = stds[2]
        tup = Tex(R"(x, y, d, \theta)")
        tup.next_to(randy.get_corner(UL), UP, buff=1)

        four_d = Text("4D Space")
        cloud = ThoughtBubble(four_d)[0][-1]
        cloud.add(four_d)
        cloud.set_width(2.5)
        cloud.next_to(randy.get_corner(UR), UP, buff=0.7).shift(0.25 * RIGHT)

        strip = ParametricSurface(mobius_strip_func)
        strip.rotate(45 * DEG, LEFT)
        strip.set_color(BLUE_D, 0.5)
        strip.set_shading(0.3, 0.4, 0)
        strip.set_width(2)
        strip.match_x(cloud).to_edge(UP, buff=MED_SMALL_BUFF)
        arrow = Arrow(strip, cloud, buff=SMALL_BUFF)

        self.play(
            morty.change("tease", randy.eyes),
            self.change_students("thinking", "erm", "pondering", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            stds[0].change("pondering", strip),
            stds[1].change("pondering", strip),
            randy.change("raise_right_hand", strip),
            ShowCreation(strip)
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(cloud, DOWN)
        )
        self.wait()
        self.play(
            stds[0].change("pondering", tup),
            stds[1].change("pondering", tup),
            randy.change("raise_left_hand", tup),
            FadeIn(tup, UP)
        )
        self.wait(5)
