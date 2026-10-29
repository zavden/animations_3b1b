# ==============================================================================
# Scene:      DefineTwoDimensional
# Source:     videos/_2017/fractal_dimension.py (lines 922-1051)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineTwoDimensional.py DefineTwoDimensional -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineTwoDimensional(PiCreatureScene):
    CONFIG = {
        "dimension" : "2",
        "length_color" : GREEN,
        "dimension_color" : YELLOW,
        "shape_width" : 2,
        "scale_factor" : 0.5,
        "bottom_shape_buff" : MED_SMALL_BUFF,
        "scalar" : "s",
    }
    def construct(self):
        self.add_title()
        self.add_h_line()
        self.add_shape()
        self.add_width_mass_labels()
        self.show_top_length()
        self.change_mode("thinking")
        self.perform_scaling()
        self.show_dimension()

    def add_title(self):
        title = OldTexText(
            self.dimension, "-dimensional",
            arg_separator = ""
        )
        self.dimension_in_title = title[0]
        self.dimension_in_title.set_color(self.dimension_color)
        title.to_edge(UP)
        self.add(title)

        self.title = title

    def add_h_line(self):
        self.h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        self.add(self.h_line)

    def add_shape(self):
        shape = self.get_shape()
        shape.set_width(self.shape_width)
        shape.next_to(self.title, DOWN, buff = MED_LARGE_BUFF)
        # self.shape.shift(FRAME_Y_RADIUS*UP/2)
        self.mass_color = shape.get_color()
        self.add(shape)

        self.shape = shape

    def add_width_mass_labels(self):
        top_length = OldTexText("Length:", "$L$")
        top_mass = OldTexText("Mass:", "$M$")
        bottom_length = OldTexText(
            "Length: ", "$%s$"%self.scalar, "$L$",
            arg_separator = ""
        )
        bottom_mass = OldTexText(
            "Mass: ",
            "$%s^%s$"%(self.scalar, self.dimension),
            "$M$",
            arg_separator = ""
        )
        self.dimension_in_exp = VGroup(
            *bottom_mass[1][-len(self.dimension):]
        )
        self.dimension_in_exp.set_color(self.dimension_color)

        top_group = VGroup(top_length, top_mass)
        bottom_group = VGroup(bottom_length, bottom_mass)
        for group in top_group, bottom_group:
            group.arrange(
                DOWN,
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )
            group[0][-1].set_color(self.length_color)
            group[1][-1].set_color(self.mass_color)

        top_group.next_to(self.h_line, UP, buff = LARGE_BUFF)
        bottom_group.next_to(self.h_line, DOWN, buff = LARGE_BUFF)
        for group in top_group, bottom_group:
            group.to_edge(LEFT)

        self.add(top_group, bottom_group)

        self.top_L = top_length[-1]
        self.bottom_L = VGroup(*bottom_length[-2:])
        self.bottom_mass = bottom_mass

    def show_top_length(self):
        brace = Brace(self.shape, LEFT)
        top_L = self.top_L.copy()

        self.play(GrowFromCenter(brace))
        self.play(top_L.next_to, brace, LEFT)
        self.wait()

        self.brace = brace

    def perform_scaling(self):
        group = VGroup(self.shape, self.brace).copy()
        self.play(
            group.shift,
            (group.get_top()[1]+self.bottom_shape_buff)*DOWN
        )

        shape, brace = group
        bottom_L = self.bottom_L.copy()
        shape.generate_target()
        shape.target.scale(
            self.scale_factor,
        )
        brace.target = Brace(shape.target, LEFT)
        self.play(*list(map(MoveToTarget, group)))
        self.play(bottom_L.next_to, brace, LEFT)
        self.wait()

    def show_dimension(self):
        top_dimension = self.dimension_in_title.copy()
        self.play(self.pi_creature.look_at, top_dimension)
        self.play(Transform(
            top_dimension,
            self.dimension_in_exp,
            run_time = 2,
        ))
        self.wait(3)

    def get_shape(self):
        return Square(
            stroke_width = 0,
            fill_color = BLUE,
            fill_opacity = 0.7,
        )
