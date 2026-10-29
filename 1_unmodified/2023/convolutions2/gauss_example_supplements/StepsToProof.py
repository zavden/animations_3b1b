# ==============================================================================
# Scene:      StepsToProof
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1056-1112)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StepsToProof.py StepsToProof -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class StepsToProof(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Steps to proving the CLT", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title, buff=-0.05, stretch_factor=1.5)
        self.add(title, underline)

        # Steps
        steps = VGroup(
            Text("""
                Step 1: Show that for all (finite variance) distribution, there exists
                some universal shape that this process will approach.
            """, t2s={"some": ITALIC}, alignment="LEFT"),
            Text("""
                Step 2: Show that the convolution of two Gaussians is another Gaussian.
            """, alignment="LEFT")
        )
        steps.set_width(0.9 * FRAME_WIDTH)
        steps.set_fill(WHITE)
        steps.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        steps.next_to(underline, DOWN, buff=0.75)

        steps[0]["(finite variance)"].set_opacity(0.7)

        # Two steps
        self.play(LaggedStartMap(
            FadeIn, VGroup(steps[0]["Step 1:"], steps[1]["Step 2:"]),
            shift=0.5 * UP,
            lag_ratio=0.5
        ))
        self.wait()

        # Step 1
        self.play(
            FadeIn(steps[0][len("Step1:"):], lag_ratio=0.01, run_time=3),
            FadeOut(steps[1]["Step 2:"]),
        )
        self.play(
            steps[0]["some universal shape"].animate.set_color(TEAL),
            lag_ratio=0.1,
        )
        self.wait()

        # Step 2
        self.play(
            FadeIn(steps[1], lag_ratio=0.01, run_time=2),
            self.frame.animate.move_to(steps, UP).shift(0.25 * UP)
        )
        texts = ["two Gaussians", "another Gaussian"]
        for text, color in zip(texts, [YELLOW, TEAL]):
            self.play(
                steps[1][text].animate.set_color(color),
                lag_ratio=0.1,
            )
            self.wait(0.5)
        self.wait()
