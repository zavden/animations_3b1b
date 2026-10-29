# ==============================================================================
# Scene:      ChooseXThenYUniformly
# Source:     videos/_2019/hyperdarts.py (lines 726-847)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChooseXThenYUniformly.py ChooseXThenYUniformly -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ChooseXThenYUniformly(Scene):
    def construct(self):
        # Setup
        unit_size = 3
        axes = Axes(
            x_min=-1.25,
            x_max=1.25,
            y_min=-1.25,
            y_max=1.25,
            axis_config={
                "tick_frequency": 0.25,
                "unit_size": unit_size,
            },
        )
        numbers = [-1, -0.5, 0.5, 1]
        num_config = {
            "num_decimal_places": 1,
            "background_stroke_width": 3,
        }
        axes.x_axis.add_numbers(
            *numbers,
            **num_config,
        )
        axes.y_axis.add_numbers(
            *numbers,
            **num_config,
            direction=LEFT,
        )

        circle = Circle(radius=unit_size)
        circle.set_stroke(WHITE, 0)
        circle.set_fill(RED, 0.7)

        square = Square()
        square.replace(circle)
        square.set_stroke(GREY_B, 1)
        square = DashedVMobject(square, num_dashes=101)

        self.add(square, circle)
        self.add(axes)

        # x and y stuff
        x_tracker = ValueTracker(-1)
        y_tracker = ValueTracker(-1)

        get_x = x_tracker.get_value
        get_y = y_tracker.get_value

        x_tip = ArrowTip(start_angle=PI / 2, color=BLUE)
        y_tip = ArrowTip(start_angle=0, color=YELLOW)
        for tip in [x_tip, y_tip]:
            tip.scale(0.5)
        x_tip.add_updater(lambda m: m.move_to(axes.c2p(get_x(), 0), UP))
        y_tip.add_updater(lambda m: m.move_to(axes.c2p(0, get_y()), RIGHT))

        x_eq = VGroup(OldTex("x = "), DecimalNumber(0))
        x_eq.arrange(RIGHT, SMALL_BUFF)
        x_eq[1].match_y(x_eq[0][0][1])
        x_eq[1].add_updater(lambda m: m.set_value(get_x()))
        x_eq.match_color(x_tip)

        y_eq = VGroup(OldTex("y = "), DecimalNumber(0))
        y_eq.arrange(RIGHT, SMALL_BUFF)
        y_eq[1].match_y(y_eq[0][0][1])
        y_eq[1].add_updater(lambda m: m.set_value(get_y()))
        y_eq.match_color(y_tip)

        eqs = VGroup(x_eq, y_eq)
        eqs.arrange(DOWN, buff=MED_LARGE_BUFF)
        eqs.to_edge(UR)

        self.add(x_tip)
        self.add(x_eq)

        # Choose x
        self.play(
            x_tracker.set_value, 1,
            run_time=2,
        )
        self.play(
            x_tracker.set_value, np.random.random(),
            run_time=1,
        )

        # Choose y
        self.play(
            FadeIn(y_tip),
            FadeIn(y_eq),
        )
        self.play(
            y_tracker.set_value, 1,
            run_time=2,
        )
        self.play(
            y_tracker.set_value, np.random.random(),
            run_time=1,
        )

        point = axes.c2p(get_x(), get_y())
        dot = Dot(point)
        x_line = DashedLine(axes.c2p(0, get_y()), point)
        y_line = DashedLine(axes.c2p(get_x(), 0), point)
        lines = VGroup(x_line, y_line)
        lines.set_stroke(WHITE, 2)

        self.play(*map(ShowCreation, lines))
        self.play(DrawBorderThenFill(dot))
        self.wait()

        points = [
            axes.c2p(*np.random.uniform(-1, 1, size=2))
            for n in range(2000)
        ]
        dots = VGroup(*[
            Dot(point, radius=0.02)
            for point in points
        ])
        self.play(
            LaggedStartMap(FadeInFromLarge, dots),
            run_time=3,
        )
        self.wait()
