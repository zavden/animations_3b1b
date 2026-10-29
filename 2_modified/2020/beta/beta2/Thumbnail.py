# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2020/beta/beta2.py (lines 2052-2111)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - NumberPlane no longer has x_line_frequency/y_line_frequency; the step-1 grid is the default (same value)
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        dartboard = Dartboard()
        axes = NumberPlane(
            x_min=-1.25,
            x_max=1.25,
            y_min=-1.25,
            y_max=1.25,
            axis_config={
                "unit_size": 0.5 * dartboard.get_width(),
                "tick_frequency": 0.25,
            },
            # CHANGE: NumberPlane no longer has x_line_frequency/y_line_frequency; the step-1 grid is the default (same value)
        )
        group = VGroup(dartboard, axes)
        group.to_edge(LEFT, buff=0)

        # Arrow
        arrow = Vector(DR, max_stroke_width_to_length_ratio=np.inf)
        arrow.move_to(axes.c2p(PI / 10, np.exp(1) / 10), DR)
        arrow.scale(1.5, about_edge=DR)
        arrow.set_stroke(WHITE, 10)

        black_arrow = arrow.copy()
        black_arrow.set_color(BLACK)
        black_arrow.set_stroke(width=20)

        arrow.get_points()[0] += 0.025 * DR

        # Coords
        coords = OldTex("(x, y) = (0.31415\\dots, 0.27182\\dots)")
        coords.set_width(5.5)
        coords.set_stroke(BLACK, 10, background=True)
        coords.next_to(axes.get_bottom(), UP, buff=0)

        # Words
        words = VGroup(
            OldTexText("Probability = 0"),
            OldTexText("$\\dots$but still possible"),
        )
        for word in words:
            word.set_width(6)
        words.arrange(DOWN, buff=MED_LARGE_BUFF)
        words.next_to(axes, RIGHT)
        words.to_edge(UP, buff=LARGE_BUFF)

        # Pi
        morty = Mortimer()
        morty.to_corner(DR)
        morty.change("confused", words)

        self.add(group)
        self.add(black_arrow)
        self.add(arrow)
        self.add(coords)
        self.add(words)
        self.add(morty)

        self.embed()
