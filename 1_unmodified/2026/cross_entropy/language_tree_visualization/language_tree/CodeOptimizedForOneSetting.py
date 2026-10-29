# ==============================================================================
# Scene:      CodeOptimizedForOneSetting
# Source:     videos/_2026/cross_entropy/language_tree_visualization/language_tree.py (lines 1032-1097)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CodeOptimizedForOneSetting.py CodeOptimizedForOneSetting -w -m --fps 15
#
# Notes:
#   ../images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo.
# ==============================================================================

from manim_imports_ext import *

PURE_MAGENTA = "#FF00FF"


class CodeOptimizedForOneSetting(InteractiveScene):
    def construct(self):
        # Add the documents
        num_docs = 20
        documents1 = VGroup(*[
            VGroup(*[
                Rectangle(
                    width=5,
                    height=1,
                    fill_opacity=1,
                    fill_color=interpolate_color(LIGHT_PINK, PURE_MAGENTA, random.random()),
                    stroke_width=0.7,
                    stroke_color=WHITE
                ).scale(0.22)
                for _ in range(8)
            ]).arrange(DOWN, buff=0)
            for _ in range(num_docs)
        ]).arrange(buff=0.75).to_edge(LEFT, buff=3.5).to_edge(UP, buff=1.1)

        documents2 = documents1.copy().to_edge(DOWN, buff=1.1)
        for doc in documents2:
            for rect in doc:
                rect.set_fill(color=interpolate_color(GREEN_B, GREEN_E, random.random()))

        self.add(documents1, documents2)

        # Add the compression arrows
        arrow1 = SVGMobject(
            "../images/arrow.svg",
            fill_opacity=1,
            fill_color=PINK
        ).rotate(-PI * 0.5).scale(0.18).next_to(documents1[0], UP, buff=0.1)
        arrow2 = arrow1.copy().flip(axis=RIGHT).next_to(documents1[0], DOWN, buff=0.1)
        arrow3 = arrow1.copy().next_to(documents2[0], UP, buff=0.1)
        arrow4 = arrow2.copy().next_to(documents2[0], DOWN, buff=0.1)
        self.add(arrow1, arrow2, arrow3, arrow4)

        # Compress the documents one by one
        for i in range(15):
            arrow1.save_state()
            arrow2.save_state()
            arrow3.save_state()
            arrow4.save_state()
            self.play(
                AnimationGroup(
                    AnimationGroup(
                        arrow1.animate.shift(DOWN * 0.65).set_color(interpolate_color(LIGHT_PINK, YELLOW, 0.3)),
                        arrow2.animate.shift(UP * 0.65).set_color(interpolate_color(LIGHT_PINK, YELLOW, 0.3)),
                        documents1[i].animate.scale(1.2).stretch(0.3, 1)
                    ),
                    AnimationGroup(
                        arrow3.animate.shift(DOWN * 0.4).set_color(interpolate_color(GREEN, YELLOW, 0.3)),
                        arrow4.animate.shift(UP * 0.4).set_color(interpolate_color(GREEN, YELLOW, 0.3)),
                        documents2[i].animate.scale(1.2).stretch(0.55, 1)
                    ), lag_ratio=0.2), run_time=0.9)
            self.play(
                AnimationGroup(
                    AnimationGroup(
                        arrow1.animate.restore(),
                        arrow2.animate.restore()
                    ),
                    AnimationGroup(
                        arrow3.animate.restore(),
                        arrow4.animate.restore()
                    ), lag_ratio=0.2), run_time=0.9)
            self.play(VGroup(documents1, documents2).animate.shift(LEFT * (documents1[1].get_x() - documents1[0].get_x())), run_time=0.8)
