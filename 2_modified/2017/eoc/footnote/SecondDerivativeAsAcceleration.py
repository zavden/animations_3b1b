# ==============================================================================
# Scene:      SecondDerivativeAsAcceleration
# Source:     videos/_2017/eoc/footnote.py (lines 678-860)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter10.py
#
# Run from this folder:
#     manimgl SecondDerivativeAsAcceleration.py SecondDerivativeAsAcceleration -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter10.py -----

def derivative(func, x, n = 1, dx = 0.01):
    samples = [func(x + (k - n/2)*dx) for k in range(n+1)]
    while len(samples) > 1:
        samples = [
            (s_plus_dx - s)/dx
            for s, s_plus_dx in zip(samples, samples[1:])
        ]
    return samples[0]



# ----- From _2017/eoc/footnote.py -----

class TrajectoryGraphScene(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10,
        "x_axis_label" : "t",
        "y_axis_label" : "s",
        # "func" : lambda x : 10*smooth(x/10.0),
        "func" : lambda t : 10*bezier([0, 0, 0, 1, 1, 1])(t/10.0),
        "color" : BLUE,
    }
    def construct(self):
        self.setup_axes()
        self.graph = self.get_graph(
            self.func,
            color = self.color
        )
        self.add(self.graph)


class SecondDerivativeAsAcceleration(Scene):
    CONFIG = {
        "car_run_time" : 6,
    }
    def construct(self):
        self.init_car_and_line()
        self.introduce_acceleration()
        self.show_functions()

    def init_car_and_line(self):
        line = Line(5.5*LEFT, 4.5*RIGHT)
        line.shift(2*DOWN)
        car = Car()
        car.move_to(line.get_left())
        self.add(line, car)
        self.car = car
        self.start_car_copy = car.copy()
        self.line = line

    def introduce_acceleration(self):
        a_words = OldTex(
            "{d^2 s \\over dt^2}(t)",  "\\Leftrightarrow",
            "\\text{Acceleration}"
        )
        a_words.set_color_by_tex("d^2 s", MAROON_B)
        a_words.set_color_by_tex("Acceleration", YELLOW)
        a_words.to_corner(UP+RIGHT )
        self.add(a_words)
        self.show_car_movement()
        self.wait()

        self.a_words = a_words

    def show_functions(self):
        def get_deriv(n):
            return lambda x : derivative(
                s_scene.graph.underlying_function, x, n
            )
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene
        s_scene = cairo_nested_scene(TrajectoryGraphScene)
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene
        v_scene = cairo_nested_scene(TrajectoryGraphScene,
            func = get_deriv(1),
            color = GREEN,
            y_max = 4,
            y_axis_label = "v",
        )
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene
        a_scene = cairo_nested_scene(TrajectoryGraphScene,
            func = get_deriv(2),
            color = MAROON_B,
            y_axis_label = "a",
            y_min = -2, 
            y_max = 2,
        )
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene
        j_scene = cairo_nested_scene(TrajectoryGraphScene,
            func = get_deriv(3),
            color = PINK,
            y_axis_label = "j",
            y_min = -2, 
            y_max = 2,
        )
        s_graph, v_graph, a_graph, j_graph = graphs = [
            VGroup(*scene.get_top_level_mobjects())
            for scene in (s_scene, v_scene, a_scene, j_scene)
        ]
        for i, graph in enumerate(graphs):
            graph.set_height(FRAME_Y_RADIUS)
            graph.to_corner(UP+LEFT)
            graph.shift(i*DOWN/2.0)

        s_words = OldTex(
            "s(t)", "\\Leftrightarrow", "\\text{Displacement}"
        )
        s_words.set_color_by_tex("s(t)", s_scene.graph.get_color())
        v_words = OldTex(
            "\\frac{ds}{dt}(t)", "\\Leftrightarrow", 
            "\\text{Velocity}"
        )
        v_words.set_color_by_tex("ds", v_scene.graph.get_color())
        j_words = OldTex(
            "\\frac{d^3 s}{dt^3}(t)", "\\Leftrightarrow", 
            "\\text{Jerk}"
        )
        j_words.set_color_by_tex("d^3", j_scene.graph.get_color())
        self.a_words.generate_target()
        words_group = VGroup(s_words, v_words, self.a_words.target, j_words)
        words_group.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        words_group.to_corner(UP+RIGHT)
        j_graph.scale(0.3).next_to(j_words, LEFT)

        positive_rect = Rectangle()
        positive_rect.set_stroke(width = 0)
        positive_rect.set_fill(GREEN, 0.5)
        positive_rect.replace(
            Line(
                a_scene.coords_to_point(0, -1),
                a_scene.coords_to_point(5, 1),
            ),
            stretch = True
        )
        negative_rect = Rectangle()
        negative_rect.set_stroke(width = 0)
        negative_rect.set_fill(RED, 0.5)
        negative_rect.replace(
            Line(
                a_scene.coords_to_point(5, 1),
                a_scene.coords_to_point(10, -1),
            ),
            stretch = True
        )

        self.show_car_movement(
            MoveToTarget(self.a_words),
            FadeIn(s_words),
            FadeIn(s_graph),
        )
        self.play(
            s_graph.scale, 0.3,
            s_graph.next_to, s_words, LEFT
        )
        self.play(*list(map(FadeIn, [v_graph, v_words])) )
        self.wait(2)
        self.play(
            v_graph.scale, 0.3,
            v_graph.next_to, v_words, LEFT
        )
        self.wait(2)
        self.play(
            Indicate(self.a_words),
            FadeIn(a_graph),
        )
        self.wait()
        self.play(FadeIn(positive_rect))
        for x in range(2):
            self.show_car_movement(
                run_time = 3,
                rate_func = lambda t : smooth(t/2.0)
            )
            self.wait()
        self.play(FadeIn(negative_rect))
        self.wait()
        self.play(MoveCar(
            self.car, self.line.get_end(),
            run_time = 3,
            rate_func = lambda t : 2*smooth((t+1)/2.0) - 1
        ))
        self.wait()
        self.play(
            a_graph.scale, 0.3,
            a_graph.next_to, self.a_words, LEFT,
            *list(map(FadeOut, [positive_rect, negative_rect]))
        )
        self.play(
            FadeOut(self.car),
            FadeIn(j_words),
            FadeIn(j_graph),
            self.line.scale, 0.5, self.line.get_left(),
            self.line.shift, LEFT,
        )
        self.car.scale(0.5)
        self.car.move_to(self.line.get_start())
        self.play(FadeIn(self.car))
        self.show_car_movement()
        self.wait(2)

    ##########

    def show_car_movement(self, *added_anims, **kwargs):
        distance = get_norm(
            self.car.get_center() - self.start_car_copy.get_center()
        )
        if distance > 1:
            self.play(FadeOut(self.car))
            self.car.move_to(self.line.get_left())
            self.play(FadeIn(self.car))

        kwargs["run_time"] = kwargs.get("run_time", self.car_run_time)
        self.play(
            MoveCar(self.car, self.line.get_right(), **kwargs),
            *added_anims
        )
