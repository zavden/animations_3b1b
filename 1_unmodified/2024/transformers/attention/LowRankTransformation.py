# ==============================================================================
# Scene:      LowRankTransformation
# Source:     videos/_2024/transformers/attention.py (lines 3014-3101)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LowRankTransformation.py LowRankTransformation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LowRankTransformation(InteractiveScene):
    def construct(self):
        # Add three sets of axes
        frame = self.frame
        frame.set_field_of_view(10 * DEGREES)

        all_axes = VGroup(
            self.get_3d_axes(),
            self.get_2d_axes(),
            self.get_3d_axes(),
        )
        all_axes.arrange(RIGHT, buff=2.0)
        all_axes.set_width(FRAME_WIDTH - 2)
        all_axes.move_to(0.5 * DOWN)
        dim_labels = VGroup(
            Text("12,288 dims"),
            Text("128 dims"),
            Text("12,288 dims"),
        )
        dim_labels.scale(0.75)
        dim_labels.set_fill(GREY_A)
        for label, axes in zip(dim_labels, all_axes):
            label.next_to(axes, UP, buff=MED_LARGE_BUFF)

        map_arrows = Tex(R"\rightarrow", font_size=96).replicate(2)
        map_arrows.set_color(YELLOW)
        for arrow, vect in zip(map_arrows, [LEFT, RIGHT]):
            arrow.next_to(all_axes[1], vect, buff=0.5)

        axes_group = VGroup(all_axes, dim_labels)
        self.add(axes_group)
        self.add(map_arrows)

        # Add vectors
        all_coords = [
            (4, 2, 1),
            (2, 3),
            (-3, 3, -2),
        ]
        colors = [BLUE, RED_B, RED_C]
        vects = VGroup(
            Arrow(axes.get_origin(), axes.c2p(*coords), buff=0, stroke_color=color)
            for axes, coords, color in zip(all_axes, all_coords, colors)
        )

        self.add(vects[0])
        for v1, v2 in zip(vects, vects[1:]):
            self.play(TransformFromCopy(v1, v2))

        for axes, vect in zip(all_axes, vects):
            axes.add(vect)
        for axes in all_axes[0::2]:
            axes.add_updater(lambda m, dt: m.rotate(2 * dt * DEGREES, axis=m.y_axis.get_vector()))
        self.wait(3)

        # Add title
        big_rect = SurroundingRectangle(axes_group, buff=0.5)
        big_rect.round_corners(radius=0.5)
        big_rect.set_stroke(RED_B, 2)
        title = Text("Low-rank transformation", font_size=72)
        title.next_to(big_rect, UP, buff=MED_LARGE_BUFF)

        self.play(
            ShowCreation(big_rect),
            FadeIn(title, shift=0.25 * UP)
        )
        self.wait(5)


    def get_3d_axes(self, height=3):
        result = ThreeDAxes((-4, 4), (-4, 4), (-4, 4))
        result.set_height(height)
        result.rotate(20 * DEGREES, DOWN)
        result.rotate(5 * DEGREES, RIGHT)
        return result

    def get_2d_axes(self, height=2):
        plane = NumberPlane(
            (-4, 4), (-4, 4),
            faded_line_ratio=0,
            background_line_style=dict(
                stroke_color=GREY_B,
                stroke_width=1,
                stroke_opacity=0.5
            )
        )
        plane.set_height(height)
        return plane
