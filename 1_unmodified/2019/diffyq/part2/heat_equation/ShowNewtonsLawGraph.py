# ==============================================================================
# Scene:      ShowNewtonsLawGraph
# Source:     videos/_2019/diffyq/part2/heat_equation.py (lines 2761-2981)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowNewtonsLawGraph.py ShowNewtonsLawGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowNewtonsLawGraph(Scene):
    CONFIG = {
        "k": 0.2,
        "initial_water_temp": 80,
        "room_temp": 20,
        "delta_T_color": YELLOW,
    }

    def construct(self):
        self.setup_axes()
        self.show_temperatures()
        self.show_graph()
        self.show_equation()
        self.talk_through_examples()

    def setup_axes(self):
        axes = Axes(
            x_min=0,
            x_max=10,
            y_min=0,
            y_max=100,
            y_axis_config={
                "unit_size": 0.06,
                "tick_frequency": 10,
            },
            center_point=5 * LEFT + 2.5 * DOWN
        )
        x_axis = axes.x_axis
        y_axis = axes.y_axis
        y_axis.add_numbers(*range(20, 100, 20))
        x_axis.add_numbers(*range(1, 11))

        x_axis.label = OldTexText("Time")
        x_axis.label.next_to(x_axis, DOWN, MED_SMALL_BUFF)

        y_axis.label = OldTex("\\text{Temperature}")
        y_axis.label.next_to(y_axis, RIGHT, buff=SMALL_BUFF)
        y_axis.label.align_to(axes, UP)
        for axis in [x_axis, y_axis]:
            axis.add(axis.label)

        self.add(axes)
        self.axes = axes

    def show_temperatures(self):
        axes = self.axes

        water_dot = Dot()
        water_dot.color_using_background_image("VerticalTempGradient")
        water_dot.move_to(axes.c2p(0, self.initial_water_temp))
        room_line = DashedLine(
            axes.c2p(0, self.room_temp),
            axes.c2p(10, self.room_temp),
        )
        room_line.set_color(BLUE)
        room_line.color_using_background_image("VerticalTempGradient")

        water_arrow = Vector(LEFT, color=WHITE)
        water_arrow.next_to(water_dot, RIGHT, SMALL_BUFF)
        water_words = OldTexText(
            "Initial water\\\\temperature"
        )
        water_words.scale(0.7)
        water_words.next_to(water_arrow, RIGHT)

        room_words = OldTexText("Room temperature")
        room_words.scale(0.7)
        room_words.next_to(room_line, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(water_dot, RIGHT),
            GrowArrow(water_arrow),
            Write(water_words),
            run_time=1,
        )
        self.play(ShowCreation(room_line))
        self.play(FadeInFromDown(room_words))
        self.wait()

        self.set_variables_as_attrs(
            water_dot,
            water_arrow,
            water_words,
            room_line,
            room_words,
        )

    def show_graph(self):
        axes = self.axes
        water_dot = self.water_dot

        k = self.k
        rt = self.room_temp
        t0 = self.initial_water_temp
        graph = axes.get_graph(
            lambda t: rt + (t0 - rt) * np.exp(-k * t)
        )
        graph.color_using_background_image("VerticalTempGradient")

        def get_x():
            return axes.x_axis.p2n(water_dot.get_center())

        brace_line = always_redraw(lambda: Line(
            axes.c2p(get_x(), rt),
            water_dot.get_center(),
            stroke_width=0,
        ))
        brace = always_redraw(
            lambda: Brace(
                brace_line, RIGHT, buff=SMALL_BUFF
            )
        )

        delta_T = OldTex("\\Delta T")
        delta_T.set_color(self.delta_T_color)
        delta_T.add_updater(lambda m: m.next_to(
            brace, RIGHT, SMALL_BUFF
        ))

        self.add(brace_line)
        self.play(
            GrowFromCenter(brace),
            Write(delta_T),
        )
        self.play(
            ShowCreation(graph),
            UpdateFromFunc(
                water_dot,
                lambda m: m.move_to(graph.get_end())
            ),
            run_time=10,
            rate_func=linear,
        )
        self.wait()

        self.graph = graph
        self.brace = brace
        self.delta_T = delta_T

    def show_equation(self):
        delta_T = self.delta_T

        equation = OldTex(
            "{d ({\\Delta T}) \\over dt} = -k \\cdot {\\Delta T}",
            tex_to_color_map={
                "{\\Delta T}": self.delta_T_color,
                "-k": WHITE,
                "=": WHITE,
            }
        )
        equation.to_corner(UR)
        equation.shift(LEFT)

        delta_T_parts = equation.get_parts_by_tex("\\Delta T")
        eq_i = equation.index_of_part_by_tex("=")
        deriv = equation[:eq_i]
        prop_to = equation.get_part_by_tex("-k")
        parts = VGroup(deriv, prop_to, delta_T_parts[1])

        words = OldTexText(
            "Rate of change",
            "is proportional to",
            "itself",
        )
        words.scale(0.7)
        words.next_to(equation, DOWN)
        colors = [BLUE, WHITE, YELLOW]
        for part, word, color in zip(parts, words, colors):
            part.word = word
            word.set_color(color)
            word.save_state()
        words[0].next_to(parts[0], DOWN)

        self.play(
            TransformFromCopy(
                VGroup(delta_T),
                delta_T_parts,
            ),
            Write(VGroup(*filter(
                lambda p: p not in delta_T_parts,
                equation
            )))
        )

        rects = VGroup()
        for part in parts:
            rect = SurroundingRectangle(
                part,
                color=part.word.get_color(),
                buff=SMALL_BUFF,
                stroke_width=2,
            )
            anims = [
                ShowCreation(rect),
                FadeIn(part.word),
            ]
            if part is parts[1]:
                anims.append(Restore(words[0]))
            self.play(*anims)
            rects.add(rect)

        self.play(FadeOut(rects, lag_ratio=0.2))

        self.equation = equation
        self.equation_words = words

    def talk_through_examples(self):
        dot = self.water_dot
        graph = self.graph

        self.play(
            MoveAlongPath(
                dot, graph,
                rate_func=lambda t: smooth(1 - t),
                run_time=2,
            )
        )

    #
    def get_slope_line(self, graph, x):
        pass
