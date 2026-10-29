# ==============================================================================
# Scene:      ManyNumberSystems
# Source:     videos/_2018/quaternions.py (lines 421-498)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyNumberSystems.py ManyNumberSystems -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyNumberSystems(Scene):
    def construct(self):
        # Too much dumb manually positioning in here...
        title = Title("Number systems")
        name_location_color_example_tuples = [
            ("Reals", [-4, 2, 0], YELLOW, "1.414"),
            ("Complex numbers", [4, 0, 0], BLUE, "2 + i"),
            ("Quaternions", [0, 2, 0], PINK, "2 + 7i + 1j + 8k"),
            ("Rationals", [3, -2, 0], RED, "1 \\over 3"),
            ("p-adic numbers", [-2, -2, 0], GREEN, "\\overline{142857}2"),
            ("Octonions", [-3, 0, 0], GREY_B, "3e_1 - 2.3e_2 + \\dots + 1.6e_8"),
        ]
        systems = VGroup()
        for name, location, color, ex in name_location_color_example_tuples:
            system = OldTexText(name)
            system.set_color(color)
            system.move_to(location)
            example = OldTex(ex)
            example.next_to(system, DOWN)
            system.add(example)
            systems.add(system)
        R_label, C_label, H_label = systems[:3]

        number_line = NumberLine(x_min=-3, x_max=3)
        number_line.add_numbers()
        number_line.shift(0.25 * FRAME_WIDTH * LEFT)
        number_line.shift(0.5 * DOWN)
        R_example_dot = Dot(number_line.number_to_point(1.414))
        plane = ComplexPlane(x_radius=3.5, y_radius=2.5)
        plane.add_coordinates()
        plane.shift(0.25 * FRAME_WIDTH * RIGHT)
        plane.shift(0.5 * DOWN)
        C_example_dot = Dot(plane.coords_to_point(2, 1))

        self.add(title)
        self.play(FadeInFromLarge(H_label))
        self.play(LaggedStartMap(
            FadeInFromLarge, VGroup(*it.chain(systems[:2], systems[3:])),
            lambda m: (m, 4)
        ))
        self.wait()
        self.add(number_line, plane, systems)
        self.play(
            R_label.move_to, 0.25 * FRAME_WIDTH * LEFT + 2 * UP,
            C_label.move_to, 0.25 * FRAME_WIDTH * RIGHT + 2 * UP,
            H_label.move_to, 0.75 * FRAME_WIDTH * RIGHT + 2 * UP,
            FadeOut(systems[3:], 2 * DOWN),
            Write(number_line),
            Write(plane),
            GrowFromCenter(R_example_dot),
            R_label[-1].next_to, R_example_dot, UP,
            GrowFromCenter(C_example_dot),
            C_label[-1].next_to, C_example_dot, UR, SMALL_BUFF,
            C_label[-1].shift, 0.4 * LEFT,
        )
        number_line.add(R_example_dot)
        plane.add(C_example_dot)
        self.wait(2)
        self.play(LaggedStartMap(
            ApplyMethod,
            VGroup(
                H_label,
                VGroup(plane, C_label),
                VGroup(number_line, R_label),
            ),
            lambda m: (m.shift, 0.5 * FRAME_WIDTH * LEFT),
            lag_ratio=0.8,
        ))
        randy = Randolph(height=1.5)
        randy.next_to(plane, RIGHT)
        randy.to_edge(DOWN)
        self.play(
            randy.change, "maybe", H_label,
            VFadeIn(randy),
        )
        self.play(Blink(randy))
        self.play(randy.change, "confused", H_label.get_top())
        self.wait()
