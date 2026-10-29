# ==============================================================================
# Scene:      AskAboutCircleProportion
# Source:     videos/outside_videos/talk_scenes.py (lines 102-142)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutCircleProportion.py AskAboutCircleProportion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutCircleProportion(Scene):
    def construct(self):
        R = 2.5
        circle = Circle(radius=R)
        circles = VGroup(circle, circle.copy())
        circles[0].move_to(R * LEFT / 2)
        circles[1].move_to(R * RIGHT / 2)
        circles[0].set_stroke(WHITE, 2)
        circles[1].set_stroke(BLUE, 4)

        dots = VGroup()
        for circle in circles:
            dots.add(Dot(circle.get_center()))

        arc = Arc(
            radius=R,
            start_angle=TAU / 3,
            angle=TAU / 3,
        )
        arc.set_stroke(YELLOW, 4)
        arc.move_arc_center_to(circles[1].get_center())

        question = OldTexText("What proportion of the circle?")
        question.set_height(0.6)
        question.to_corner(UL)
        arrow = Arrow(
            question.get_bottom() + LEFT,
            arc.point_from_proportion(0.25),
        )

        self.add(circles)
        self.add(dots)
        self.add(arc)
        self.add(question)
        self.add(arrow)

        answer = OldTex("1/3")
        answer.set_height(0.9)
        answer.set_color(YELLOW)
        answer.next_to(question, RIGHT, LARGE_BUFF)
        self.add(answer)
