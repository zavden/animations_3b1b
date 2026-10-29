# ==============================================================================
# Scene:      RepeatedTextSegments
# Source:     videos/_2026/cross_entropy/language_tree_visualization/language_tree.py (lines 1100-1145)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RepeatedTextSegments.py RepeatedTextSegments -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RepeatedTextSegments(InteractiveScene):
    def construct(self):
        # Add the text
        text = Text(
            """
                In the dark, dark
                wood, there was a dark, dark
                house. And in that dark, dark
                house, there was a dark, dark
                room. And in that dark, dark
                room, there was a dark, dark
                cupboard. And in that dark, dark
                cupboard, there was a dark, dark
                shelf. And on that dark, dark
                shelf, there was a dark, dark
                box. And in that dark, dark
                box, there was a ghost.
                Hoo-hoo-hoo! Haa-haa-boo!
            """,
            font_size=35
        ).to_edge(RIGHT, buff=1)
        self.add(text)

        # Highlight the repeated segments
        self.wait(1)
        self.play(text["dark, dark"].animate.set_color(TEAL), run_time=1, lag_ratio=0.2)
        self.wait(2)

        # Replace them with pointers
        dots = VGroup(*[
            Dot().set_color(TEAL).move_to(darkdark)
            for darkdark in text["dark, dark"][1:]
        ])
        pointers = VGroup(*[
            CurvedArrow(dot.get_center(), text["dark, dark"][0].get_right(), angle=0.3 * PI + PI * i * 0.05).set_color(YELLOW).set_stroke(opacity=0.7)
            for i, dot in enumerate(dots)
        ])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    FadeIn(darkdark.copy().set_opacity(0.2), run_time=0.4),
                    TransformMatchingShapes(darkdark, dot)
                )
                for darkdark, dot in zip(text["dark, dark"][1:], dots)
            ], lag_ratio=0.1), run_time=1.5)
        self.play(AnimationGroup(*[GrowArrow(pointer) for pointer in pointers], lag_ratio=0.1), run_time=2)
