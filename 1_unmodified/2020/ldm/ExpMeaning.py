# ==============================================================================
# Scene:      ExpMeaning
# Source:     videos/_2020/ldm.py (lines 659-749)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpMeaning.py ExpMeaning -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import math

class ExpMeaning(Scene):
    CONFIG = {
        "include_circle": True
    }

    def construct(self):
        # Plane
        plane = ComplexPlane(y_min=-6, y_max=6)
        plane.shift(1.5 * DOWN)
        plane.add_coordinates()
        if self.include_circle:
            circle = Circle(radius=1)
            circle.set_stroke(RED, 1)
            circle.move_to(plane.n2p(0))
            plane.add(circle)

        # Equation
        equation = OldTex(
            "\\text{exp}(i\\theta) = ",
            "1 + ",
            "i\\theta + ",
            "{(i\\theta)^2 \\over 2} + ",
            "{(i\\theta)^3 \\over 6} + ",
            "{(i\\theta)^4 \\over 24} + ",
            "\\cdots",
            tex_to_color_map={
                "\\theta": YELLOW,
                "i": GREEN,
            },
        )
        equation.add_background_rectangle(buff=MED_SMALL_BUFF, opacity=1)
        equation.to_edge(UL, buff=0)

        # Label
        theta_tracker = ValueTracker(0)
        theta_label = VGroup(
            OldTex("\\theta = "),
            DecimalNumber(0, num_decimal_places=4)
        )
        theta_decimal = theta_label[1]
        theta_decimal.add_updater(
            lambda m, tt=theta_tracker: m.set_value(tt.get_value())
        )
        theta_label.arrange(RIGHT, buff=SMALL_BUFF)
        theta_label.set_color(YELLOW)
        theta_label.add_to_back(BackgroundRectangle(
            theta_label,
            buff=MED_SMALL_BUFF,
            fill_opacity=1,
        ))
        theta_label.next_to(equation, DOWN, aligned_edge=LEFT, buff=0)

        # Vectors
        def get_vectors(n_vectors=20, plane=plane, tracker=theta_tracker):
            last_tip = plane.n2p(0)
            z = complex(0, tracker.get_value())
            vects = VGroup()
            colors = color_gradient([GREEN, YELLOW, RED], 6)
            for i, color in zip(range(n_vectors), it.cycle(colors)):
                vect = Vector(complex_to_R3(z**i / math.factorial(i)))
                vect.set_color(color)
                vect.shift(last_tip)
                last_tip = vect.get_end()
                vects.add(vect)
            return vects

        vectors = always_redraw(get_vectors)
        dot = Dot()
        dot.set_height(0.03)
        dot.add_updater(lambda m, vs=vectors: m.move_to(vs[-1].get_end()))

        self.add(plane)
        self.add(vectors)
        self.add(dot)
        self.add(equation)
        self.add(theta_label)

        self.play(
            theta_tracker.set_value, 1,
            run_time=3,
            rate_func=smooth,
        )
        self.wait()
        for target in PI, TAU:
            self.play(
                theta_tracker.set_value, target,
                run_time=10,
            )
            self.wait()

        self.embed()
