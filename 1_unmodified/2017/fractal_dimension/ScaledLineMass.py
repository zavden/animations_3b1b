# ==============================================================================
# Scene:      ScaledLineMass
# Source:     videos/_2017/fractal_dimension.py (lines 802-882)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ScaledLineMass.py ScaledLineMass -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ScaledLineMass(Scene):
    CONFIG = {
        "title" : "Line",
        "mass_scaling_factor" : "\\frac{1}{2}",
        "shape_width" : 2,
        "break_up_factor" : 1.3,
        "vert_distance" : 2,
        "brace_direction" : DOWN,
        "shape_to_shape_buff" : 2*LARGE_BUFF,
    }
    def construct(self):
        title = OldTexText(self.title)
        title.to_edge(UP)
        scaling_factor_label = OldTexText(
            "Scaling factor:", "$\\frac{1}{2}$"
        )
        scaling_factor_label[1].set_color(YELLOW)
        scaling_factor_label.to_edge(LEFT).shift(UP)
        mass_scaling_label = OldTexText(
            "Mass scaling factor:", "$%s$"%self.mass_scaling_factor
        )
        mass_scaling_label[1].set_color(GREEN)
        mass_scaling_label.next_to(
            scaling_factor_label, DOWN,
            aligned_edge = LEFT,
            buff = LARGE_BUFF
        )

        shape = self.get_shape()
        shape.set_width(self.shape_width)
        shape.center()
        shape.shift(FRAME_X_RADIUS*RIGHT/2 + self.vert_distance*UP)

        big_brace = Brace(shape, self.brace_direction)
        big_brace_text = big_brace.get_text("$1$")

        shape_copy = shape.copy()
        shape_copy.next_to(shape, DOWN, buff = self.shape_to_shape_buff)
        shape_copy.scale(self.break_up_factor)
        for submob in shape_copy:
            submob.scale(1./self.break_up_factor)

        little_brace = Brace(shape_copy[0], self.brace_direction)
        little_brace_text = little_brace.get_text("$\\frac{1}{2}$")

        self.add(title, scaling_factor_label, mass_scaling_label[0])
        self.play(GrowFromCenter(shape))
        self.play(
            GrowFromCenter(big_brace),
            Write(big_brace_text)
        )
        self.wait()

        self.play(
            shape.copy().replace, shape_copy[0]
        )
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(shape_copy[0])
        self.play(
            GrowFromCenter(little_brace),
            Write(little_brace_text)
        )
        self.wait()

        self.play(Write(mass_scaling_label[1], run_time = 1))
        self.wait()
        self.play(FadeIn(
            VGroup(*shape_copy[1:]),
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(Transform(
            shape_copy.copy(), shape
        ))
        self.wait()

    def get_shape(self):
        return VGroup(
            Line(LEFT, ORIGIN),
            Line(ORIGIN, RIGHT)
        ).set_color(BLUE)
