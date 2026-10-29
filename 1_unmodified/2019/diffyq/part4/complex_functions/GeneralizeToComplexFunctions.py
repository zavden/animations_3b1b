# ==============================================================================
# Scene:      GeneralizeToComplexFunctions
# Source:     videos/_2019/diffyq/part4/complex_functions.py (lines 4-254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralizeToComplexFunctions.py GeneralizeToComplexFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralizeToComplexFunctions(Scene):
    CONFIG = {
        "axes_config": {
            "x_min": 0,
            "x_max": 10,
            "x_axis_config": {
                "stroke_width": 2,
            },
            "y_min": -2.5,
            "y_max": 2.5,
            "y_axis_config": {
                "tick_frequency": 0.25,
                "unit_size": 1.5,
                "include_tip": False,
                "stroke_width": 2,
            },
        },
        "complex_plane_config": {
            "axis_config": {
                "unit_size": 2
            }
        },
    }

    def construct(self):
        self.show_cosine_wave()
        self.transition_to_complex_plane()
        self.add_rotating_vectors_making_cos()

    def show_cosine_wave(self):
        axes = Axes(**self.axes_config)
        axes.shift(2 * LEFT - axes.c2p(0, 0))
        y_axis = axes.y_axis
        y_labels = y_axis.get_number_mobjects(
            *range(-2, 3),
            num_decimal_places=1
        )

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda t, dt: t.increment_value(dt))
        get_t = t_tracker.get_value

        def func(x):
            return 2 * np.cos(x)

        cos_x_max = 20
        cos_wave = axes.get_graph(func, x_max=cos_x_max)
        cos_wave.set_color(YELLOW)
        shown_cos_wave = cos_wave.copy()
        shown_cos_wave.add_updater(
            lambda m: m.pointwise_become_partial(
                cos_wave, 0,
                np.clip(get_t() / cos_x_max, 0, 1),
            ),
        )

        dot = Dot()
        dot.set_color(PINK)
        dot.add_updater(lambda d: d.move_to(
            y_axis.n2p(func(get_t())),
        ))

        h_line = always_redraw(lambda: Line(
            dot.get_right(),
            shown_cos_wave.get_end(),
            stroke_width=1,
        ))

        real_words = OldTexText(
            "Real number\\\\output"
        )
        real_words.to_edge(LEFT)
        real_words.shift(2 * UP)
        real_arrow = Arrow()
        real_arrow.add_updater(
            lambda m: m.put_start_and_end_on(
                real_words.get_corner(DR),
                dot.get_center(),
            ).scale(0.9),
        )

        self.add(t_tracker)
        self.add(axes)
        self.add(y_labels)
        self.add(shown_cos_wave)
        self.add(dot)
        self.add(h_line)

        self.wait(2)
        self.play(
            FadeIn(real_words, RIGHT),
            FadeIn(real_arrow),
        )
        self.wait(5)

        y_axis.generate_target()
        y_axis.target.rotate(-90 * DEGREES)
        y_axis.target.center()
        y_axis.target.scale(2 / 1.5)
        y_labels.generate_target()
        for label in y_labels.target:
            label.next_to(
                y_axis.target.n2p(label.get_value()),
                DOWN, MED_SMALL_BUFF,
            )
        self.play(
            FadeOut(shown_cos_wave),
            FadeOut(axes.x_axis),
            FadeOut(h_line),
        )
        self.play(
            MoveToTarget(y_axis),
            MoveToTarget(y_labels),
            real_words.shift, 2 * RIGHT + UP,
        )
        self.wait()

        self.y_axis = y_axis
        self.y_labels = y_labels
        self.real_words = real_words
        self.real_arrow = real_arrow
        self.dot = dot
        self.t_tracker = t_tracker

    def transition_to_complex_plane(self):
        y_axis = self.y_axis
        y_labels = self.y_labels

        plane = self.get_complex_plane()
        plane_words = plane.label

        self.add(plane, *self.get_mobjects())
        self.play(
            FadeOut(y_labels),
            FadeOut(y_axis),
            ShowCreation(plane),
        )
        self.play(Write(plane_words))
        self.wait()

        self.plane = plane
        self.plane_words = plane_words

    def add_rotating_vectors_making_cos(self):
        plane = self.plane
        real_words = self.real_words
        real_arrow = self.real_arrow
        t_tracker = self.t_tracker
        get_t = t_tracker.get_value

        v1 = Vector(2 * RIGHT)
        v2 = Vector(2 * RIGHT)
        v1.set_color(BLUE)
        v2.set_color(interpolate_color(GREY_BROWN, WHITE, 0.5))
        v1.add_updater(
            lambda v: v.set_angle(get_t())
        )
        v2.add_updater(
            lambda v: v.set_angle(-get_t())
        )
        v1.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )
        # Change?
        v2.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )

        ghost_v1 = v1.copy()
        ghost_v1.set_opacity(0.5)
        ghost_v1.add_updater(
            lambda v: v.shift(
                v2.get_end() - v.get_start()
            )
        )

        ghost_v2 = v2.copy()
        ghost_v2.set_opacity(0.5)
        ghost_v2.add_updater(
            lambda v: v.shift(
                v1.get_end() - v.get_start()
            )
        )

        circle = Circle(color=GREY_BROWN)
        circle.set_stroke(width=1)
        circle.set_width(2 * v1.get_length())
        circle.move_to(plane.n2p(0))

        formula = OldTex(
            # "\\cos(x) ="
            # "{1 \\over 2}e^{ix} +"
            # "{1 \\over 2}e^{-ix}",
            "2\\cos(x) =",
            "e^{ix}", "+", "e^{-ix}",
            tex_to_color_map={
                "e^{ix}": v1.get_color(),
                "e^{-ix}": v2.get_color(),
            }
        )
        formula.next_to(ORIGIN, UP, buff=0.75)
        # formula.add_background_rectangle()
        formula.set_stroke(BLACK, 3, background=True)
        formula.to_edge(LEFT, buff=MED_SMALL_BUFF)
        formula_brace = Brace(formula[1:], UP)
        formula_words = formula_brace.get_text(
            "Sum of\\\\rotations"
        )
        formula_words.set_stroke(BLACK, 3, background=True)

        randy = Randolph()
        randy.to_corner(DL)
        randy.look_at(formula)

        self.play(
            FadeOut(real_words),
            FadeOut(real_arrow),
        )
        self.play(
            FadeIn(v1),
            FadeIn(v2),
            FadeIn(circle),
            FadeIn(ghost_v1),
            FadeIn(ghost_v2),
        )
        self.wait(3)
        self.play(FadeInFromDown(formula))
        self.play(
            GrowFromCenter(formula_brace),
            FadeIn(formula_words),
        )
        self.wait(2)
        self.play(FadeIn(randy))
        self.play(randy.change, "pleading")
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change, "confused")
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy))
        self.wait(20)

    #
    def get_complex_plane(self):
        plane = ComplexPlane(**self.complex_plane_config)
        plane.add_coordinates()

        plane.label = OldTexText("Complex plane")
        plane.label.scale(1.5)
        plane.label.to_corner(UR, buff=MED_SMALL_BUFF)
        return plane
