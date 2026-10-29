# ==============================================================================
# Scene:      ProofInsideUnderstanding
# Source:     videos/_2026/2025_p6/problem_intro.py (lines 637-683)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProofInsideUnderstanding.py ProofInsideUnderstanding -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProofInsideUnderstanding(InteractiveScene):
    def construct(self):
        # Test
        Checkmark()
        frame = self.frame
        circles = VGroup(
            Circle(radius=4).set_fill(BLUE_E, 0.5).set_stroke(BLUE_E, 2).center(),
            Circle(radius=1).set_fill(TEAL, 0.5).set_stroke(TEAL, 2).move_to(2 * LEFT),
        )
        titles = VGroup(
            Text("Understanding", font_size=60).next_to(circles[0].get_top(), DOWN, LARGE_BUFF),
            Text("Proof", font_size=36).next_to(circles[1].get_top(), DOWN, MED_LARGE_BUFF),
        )

        frame.set_height(4).move_to(circles[1])
        self.play(
            Write(circles[1]),
            Write(titles[1]),
            run_time=1
        )
        self.wait()
        self.add(*circles, *titles)
        self.play(
            frame.animate.to_default_state(),
            Write(circles[0]),
            Write(titles[0]),
            run_time=2
        )
        self.wait()

        # Add words
        frame.center().set_height(10)
        text = VGroup(
            Text("How do we shift\nacademic credit\nfrom here...", font_size=48, alignment="LEFT"),
            Text("...to here", font_size=48),
        )
        text[0].next_to(circles, LEFT).shift(2 * UP)
        text[1].next_to(circles, RIGHT, LARGE_BUFF).shift(2 * DOWN)

        arrows = VGroup(
            Arrow(text[0].get_bottom(), circles[1].get_center(), thickness=5, path_arc=90 * DEG, buff=0.5),
            Arrow(text[1].get_top(), circles[0].get_center() + RIGHT, thickness=5, path_arc=90 * DEG, buff=0.5),
        )

        VGroup(text, arrows).set_color(YELLOW)

        self.add(text, arrows)
