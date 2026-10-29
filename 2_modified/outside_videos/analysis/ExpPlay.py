# ==============================================================================
# Scene:      ExpPlay
# Source:     videos/outside_videos/analysis.py (lines 12-139)
# Category:   2 · Renders with modifications
# Includes code copied from: _2016/zeta.py
#
# Run from this folder:
#     manimgl ExpPlay.py ExpPlay -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve: t_min/t_max -> t_range=(min, max, step)
#   - NumberLine: x_min/x_max -> x_range
#   - old syntax self.play(mob.method, args) -> mob.animate.method(args)
# ==============================================================================

from manim_imports_ext import *
import mpmath


# ----- From _2016/zeta.py -----

mpmath.mp.dps = 7



# ----- From outside_videos/analysis.py -----

def approx_exp(x, n):
    return sum([
        x**k / math.factorial(k)
        for k in range(n + 1)
    ])


class ExpPlay(Scene):
    def construct(self):
        for n in [2, 4, 6, 8, 10]:
            self.show_sum_up_to(n)
            self.clear()
        self.show_sum_up_to(40, 10, include_dots=True)
        self.wait(2)

    def show_sum_up_to(self, n, shown_n=None, include_dots=False):
        plane = ComplexPlane()
        plane.add_coordinate_labels()
        self.add(plane)
        plane.shift(DOWN)

        if shown_n is None:
            shown_n = n

        t_tracker = ValueTracker(0)
        vectors = always_redraw(
            lambda: self.get_sum_vectors(
                t_tracker.get_value(),
                n,
                center=plane.n2p(0),
            )
        )

        # CHANGE: ParametricCurve: t_min/t_max -> t_range=(min, max, step)
        path = ParametricCurve(
            lambda t: plane.n2p(approx_exp(complex(0, t), n)),
            t_range=(0, TAU, 0.01),
        )
        path.set_color(WHITE)

        formula = OldTex(
            "e^{it} \\approx",
            *[
                "{(ti)^{%d} \\over %d!} +" % (k, k)
                for k in range(shown_n + 1)
            ],
            "\\cdots" if include_dots else "",
        )
        for vect, part in zip(vectors, formula[1:]):
            part.match_color(vect)
            part[-1].set_color(WHITE)

        if include_dots:
            formula[-1].set_color(WHITE)
        else:
            formula[-1][-1].set_opacity(0)

        if formula.get_width() > FRAME_WIDTH - 1:
            formula.set_width(FRAME_WIDTH - 1)
        formula.to_edge(UP, buff=MED_SMALL_BUFF)
        formula.set_stroke(BLACK, 5, background=True)
        formula.add_background_rectangle(buff=MED_SMALL_BUFF)

        # CHANGE: NumberLine: x_min/x_max -> x_range
        number_line = NumberLine(
            x_range=(0, 7.5, 1),
        )
        number_line.set_width(5)
        number_line.add_numbers()
        number_line.move_to(1.25 * UP)
        number_line.to_edge(RIGHT)
        rect = BackgroundRectangle(number_line, buff=MED_SMALL_BUFF)
        rect.stretch(2, 1, about_edge=DOWN)
        rect.set_width(7, stretch=True)
        tip = ArrowTip()
        tip.rotate(-PI / 2)
        tip.set_color(WHITE)
        tip.add_updater(
            lambda m: m.move_to(
                number_line.n2p(t_tracker.get_value()),
                DOWN,
            )
        )
        t_eq = VGroup(
            OldTex("t="),
            DecimalNumber(0),
        )
        t_eq.add_updater(lambda m: m.arrange(RIGHT, buff=SMALL_BUFF))
        t_eq.add_updater(lambda m: m.next_to(tip, UP, SMALL_BUFF))
        t_eq.add_updater(lambda m: m[1].set_value(t_tracker.get_value()))

        self.add(rect, number_line, tip, t_eq)

        self.add(vectors, path, formula)
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(
            t_tracker.animate.set_value(TAU),
            ShowCreation(path),
            run_time=4,
            rate_func=bezier([0, 0, 1, 1]),
        )
        self.wait()

    def get_sum_vectors(self, t, n, center=ORIGIN):
        vectors = VGroup()
        template_vect = Vector(RIGHT)
        last_tip = center
        for k in range(n + 1):
            vect = template_vect.copy()
            vect.rotate(k * PI / 2)
            vect.scale(t**k / math.factorial(k))
            vect.set_stroke(
                width=max(2, vect.get_stroke_width())
            )
            # vect.tip.set_stroke(width=0)
            vect.shift(last_tip - vect.get_start())
            last_tip = vect.get_end()
            vectors.add(vect)
        self.color_vectors(vectors)
        return vectors

    def color_vectors(self, vectors, colors=[BLUE, YELLOW, RED, PINK]):
        for vect, color in zip(vectors, it.cycle(colors)):
            vect.set_color(color)

    def get_paths(self):
        paths = VGroup(*[
            ParametricCurve(
                lambda t: plane.n2p(approx_exp(complex(0, t), n)),
                t_min=-PI,
                t_max=PI,
            )
            for n in range(10)
        ])
        paths.set_color_by_gradient(BLUE, YELLOW, RED)
        return paths
