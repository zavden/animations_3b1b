# ==============================================================================
# Scene:      InfiniteCircleScene
# Source:     videos/_2018/basel/basel.py (lines 4382-4457)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InfiniteCircleScene.py InfiniteCircleScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class InfiniteCircleScene(PiCreatureScene):

    def construct(self):

        morty = self.get_primary_pi_creature()
        morty.set_color(MAROON_D).flip()
        morty.color = MAROON_D
        morty.scale(0.5).move_to(ORIGIN)

        arrow = Arrow(ORIGIN, 2.4 * RIGHT)
        dot = Dot(color = BLUE).next_to(arrow)
        ellipsis = OldTex("\dots")

        infsum = VGroup()
        infsum.add(ellipsis.copy())

        for i in range(3):
            infsum.add(arrow.copy().next_to(infsum.submobjects[-1]))
            infsum.add(dot.copy().next_to(infsum.submobjects[-1]))

        infsum.add(arrow.copy().next_to(infsum.submobjects[-1]))
        infsum.add(ellipsis.copy().next_to(infsum.submobjects[-1]))

        infsum.next_to(morty,DOWN, buff = 1)

        self.wait()
        self.play(
            LaggedStartMap(FadeIn,infsum,lag_ratio = 0.2)
        )
        self.wait()

        A = infsum.submobjects[-1].get_center() + 0.5 * RIGHT
        B = A + RIGHT + 1.3 * UP + 0.025 * LEFT
        right_arc = DashedLine(TAU/4*UP, ORIGIN, stroke_color = YELLOW,
            stroke_width = 8).apply_complex_function(np.exp)
        right_arc.rotate(-TAU/4).next_to(infsum, RIGHT).shift(0.5 * UP)
        right_tip_line = Arrow(B - UP, B, color = WHITE)
        right_tip_line.add_tip()
        right_tip = right_tip_line.get_tip()
        right_tip.set_fill(color = YELLOW)
        right_arc.add(right_tip)
        

        C = B + 3.2 * UP
        right_line = DashedLine(B + 0.2 * DOWN,C + 0.2 * UP, stroke_color = YELLOW,
            stroke_width = 8)

        ru_arc = right_arc.copy().rotate(angle = TAU/4)
        ru_arc.remove(ru_arc.submobjects[-1])
        ru_arc.to_edge(UP+RIGHT, buff = 0.15)

        D = np.array([5.85, 3.85,0])
        E = np.array([-D[0],D[1],0])
        up_line = DashedLine(D, E, stroke_color = YELLOW,
            stroke_width = 8)

        lu_arc = ru_arc.copy().flip().to_edge(LEFT + UP, buff = 0.15)
        left_line = right_line.copy().flip(axis = RIGHT).to_edge(LEFT, buff = 0.15)

        left_arc = right_arc.copy().rotate(-TAU/4)
        left_arc.next_to(infsum, LEFT).shift(0.5 * UP + 0.1 * LEFT)

        right_arc.shift(0.2 * RIGHT)
        right_line.shift(0.2 * RIGHT)

        self.play(FadeIn(right_arc))
        self.play(ShowCreation(right_line))
        self.play(FadeIn(ru_arc))
        self.play(ShowCreation(up_line))
        self.play(FadeIn(lu_arc))
        self.play(ShowCreation(left_line))
        self.play(FadeIn(left_arc))



        self.wait()
