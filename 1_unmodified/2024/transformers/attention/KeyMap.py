# ==============================================================================
# Scene:      KeyMap
# Source:     videos/_2024/transformers/attention.py (lines 1839-1847)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyMap.py KeyMap -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class QueryMap(InteractiveScene):
    map_tex = "W_Q"
    map_color = YELLOW
    src_name = "Creature"
    pos_word = "position 4"
    trg_name = "Any adjectives\nbefore position 4?"
    in_vect_color = BLUE_B
    in_vect_coords = (3, 2, -2)
    out_vect_coords = (-2, -1)

    def construct(self):
        # Setup 3d axes
        axes_3d = ThreeDAxes((-4, 4), (-3, 3), (-4, 4))
        xz_plane = NumberPlane(
            (-4, 4), (-4, 4),
            background_line_style=dict(
                stroke_color=GREY,
                stroke_width=1,
            ),
            faded_line_ratio=0
        )
        xz_plane.rotate(90 * DEGREES, RIGHT)
        xz_plane.move_to(axes_3d)
        xz_plane.axes.set_opacity(0)
        axes_3d.add(xz_plane)
        axes_3d.set_height(2.0)

        self.set_floor_plane("xz")
        frame = self.frame
        frame.set_field_of_view(30 * DEGREES)
        frame.reorient(-32, 0, 0, (2.13, 1.11, 0.27), 4.50)
        frame.add_ambient_rotation(1 * DEGREES)

        self.add(axes_3d)

        # Set up target plane
        plane = NumberPlane(
            (-3, 3), (-3, 3),
            faded_line_ratio=1,
            background_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.75
            ),
            faded_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.25,
            )
        )
        plane.set_height(3.5)
        plane.to_corner(DR)

        arrow = Tex(R"\longrightarrow")
        arrow.set_width(2)
        arrow.stretch(0.75, 1)
        arrow.next_to(plane, LEFT, buff=1.0)
        arrow.set_color(self.map_color)

        map_name = Tex(self.map_tex, font_size=72)
        map_name.set_color(self.map_color)
        map_name.next_to(arrow.get_left(), UR, SMALL_BUFF).shift(0.25 * RIGHT)

        for mob in [plane, arrow, map_name]:
            mob.fix_in_frame()

        self.add(plane)
        self.add(arrow)
        self.add(map_name)

        # Add titles
        titles = VGroup(
            Text("Embedding space"),
            Text("Query/Key space"),
        )
        subtitles = VGroup(
            Text("12,288-dimensional"),
            Text("128-dimensional"),
        )
        subtitles.scale(0.75)
        subtitles.set_fill(GREY_B)
        x_values = [-frame.get_x() * FRAME_HEIGHT / frame.get_height(), plane.get_x()]
        for title, subtitle, x_value in zip(titles, subtitles, x_values):
            subtitle.next_to(title, DOWN, SMALL_BUFF)
            title.add(subtitle)
            title.next_to(plane, UP, MED_LARGE_BUFF)
            title.set_x(x_value)
            title.fix_in_frame()

        self.add(titles)

        # Show vector transformation
        in_vect = Arrow(axes_3d.get_origin(), axes_3d.c2p(*self.in_vect_coords), buff=0)
        in_vect.set_stroke(self.in_vect_color)
        in_vect_label = TexText("``" + self.src_name + "''", font_size=24)
        pos_label = Text(self.pos_word, font_size=16)
        pos_label.next_to(in_vect_label, DOWN, SMALL_BUFF)
        pos_label.set_opacity(0.75)
        in_vect_label.add(pos_label)
        in_vect_label.set_color(self.in_vect_color)
        in_vect_label.next_to(in_vect.get_end(), UP, SMALL_BUFF)

        out_vect = Arrow(plane.get_origin(), plane.c2p(*self.out_vect_coords), buff=0)
        out_vect.set_stroke(self.map_color)
        out_vect_label = Text(self.trg_name, font_size=30)
        out_vect_label.next_to(out_vect.get_end(), DOWN, buff=0.2)
        out_vect_label.set_backstroke(BLACK, 5)
        VGroup(out_vect, out_vect_label).fix_in_frame()

        self.play(
            GrowArrow(in_vect),
            FadeInFromPoint(in_vect_label, axes_3d.get_origin()),
        )
        self.wait(2)
        self.play(
            TransformFromCopy(in_vect, out_vect),
            FadeTransform(in_vect_label.copy(), out_vect_label),
            run_time=2,
        )
        self.wait(20)
        self.play(FadeOut(out_vect_label))
        self.wait(5)


class KeyMap(QueryMap):
    map_tex = "W_K"
    map_color = TEAL
    src_name = "Fluffy"
    pos_word = "position 2"
    trg_name = "Adjective at\nposition 2"
    in_vect_color = BLUE_B
    in_vect_coords = (-3, 1, 2)
    out_vect_coords = (-1.75, -1)
