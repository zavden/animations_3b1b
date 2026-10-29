# ==============================================================================
# Scene:      HighLevelCLTDescription
# Source:     videos/_2023/clt/wordy_scenes.py (lines 432-510)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighLevelCLTDescription.py HighLevelCLTDescription -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HighLevelCLTDescription(InteractiveScene):
    def construct(self):
        # Title
        title = Text("General idea of the Central Limit Theorem", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title["Central Limit Theorem"].set_color(YELLOW)
        underline = Underline(title)
        underline.scale(1.2)
        underline.set_stroke(WHITE, [0, 3, 3, 0])
        self.add(title)
        self.play(ShowCreation(underline))
        self.wait()

        # Random variables
        kw = dict(font_size=42)
        words = TexText("Start with a random variable: $X$", **kw)
        words["random variable: $X$"].set_color(BLUE)
        sub_words = Text("""
            (a random process, where each outcome
            is associated with some number)
        """, font_size=32)
        sub_words.next_to(words, DOWN)
        sub_words.set_color(GREY_A)

        point1 = VGroup(words, sub_words)
        point1.next_to(underline, DOWN, buff=0.7)
        point1.to_edge(LEFT, buff=MED_SMALL_BUFF)

        example_boxes = Square().replicate(2)
        example_boxes.set_height(1.75)
        example_boxes.set_width(2.25, stretch=True)
        example_boxes.arrange(RIGHT, buff=1)
        example_boxes.set_stroke(WHITE, 1)
        example_boxes.match_y(point1)
        example_boxes.to_edge(RIGHT)

        self.play(
            Write(words, run_time=1, stroke_width=1),
            LaggedStartMap(FadeIn, example_boxes, lag_ratio=0.5),
        )
        self.wait()
        self.play(FadeIn(sub_words, 0.25 * DOWN))
        self.wait()

        # Sample many
        point2 = TexText(R"""
            Add $N$ samples of this variable \\
            $X_1 + X_2 + \cdots + X_N$
        """, **kw)
        point2["$N$ samples"].set_color(RED)
        point2[R"$X_1 + X_2 + \cdots + X_N$"].set_color(BLUE).shift(0.25 * DOWN)
        point2.next_to(point1, DOWN, buff=1.1, aligned_edge=LEFT)

        example_boxes2 = example_boxes.copy()
        example_boxes2.match_y(point2)

        self.play(
            FadeIn(point2, DOWN),
            FadeIn(example_boxes2, DOWN),
        )
        self.wait()

        # Distribution
        point3 = TexText(R"""
            The distribution of this sum looks \\
            more like a bell curve as $N \to \infty$
        """, **kw)
        point3["this sum"].set_color(BLUE)
        point3["bell curve"].set_color(YELLOW)
        point3[R"$N \to \infty$"].set_color(RED)
        point3.next_to(point2, DOWN, buff=1.25, aligned_edge=LEFT)
        example_boxes3 = example_boxes.copy()
        example_boxes3.match_y(point3)

        self.play(
            FadeIn(point3, DOWN),
            FadeIn(example_boxes3, DOWN),
        )
        self.wait()
