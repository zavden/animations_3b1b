# ==============================================================================
# Scene:      AskAboutAddingThetaToItselfThetaPoint2
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 488-492)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAddingThetaToItselfThetaPoint2.py AskAboutAddingThetaToItselfThetaPoint2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutAddingThetaToItself(Scene):
    CONFIG = {
        "theta": np.arctan(0.25),
        "wait_time": 0.25,
        "wedge_radius": 3,
        "theta_symbol_scale_val": 0.5,
        "number_height": 0.2,
    }

    def construct(self):
        theta = self.theta
        groups = self.get_groups(theta)
        horizon = self.get_horizon()
        counter = ValueTracker(0)
        dynamic_ineq = self.get_dynamic_inequality(counter)
        semicircle = self.get_semicircle()

        self.add(horizon)
        self.add(dynamic_ineq)

        for n in range(len(groups)):
            counter.set_value(n + 1)
            if n < len(groups) - 1:
                groups[n][-1].set_color(YELLOW)
                if n > 0:
                    groups[n - 1][-1].set_color(WHITE)
            self.add(groups[:n + 1])
            self.add_sound("pen_click", gain=-20)
            self.wait(self.wait_time)
        self.wait(0.5)

        counter.set_value(counter.get_value() - 1)
        self.remove(groups[-1])
        self.add_sound("pen_click", gain=-20)
        self.wait()

        self.play(ShowCreation(semicircle))
        self.play(FadeOut(semicircle))

        self.wait(3)

    def get_group(self, theta):
        # Define group
        wedge_radius = self.wedge_radius
        wedge = VGroup(
            Line(ORIGIN, wedge_radius * RIGHT),
            Line(ORIGIN, wedge_radius * RIGHT).rotate(
                theta, about_point=ORIGIN
            ),
        )
        wedge.set_stroke((WHITE, GREY), 2)
        arc = Arc(theta, radius=1)
        theta_symbol = OldTex("\\theta")
        tssv = self.theta_symbol_scale_val
        theta_symbol.scale(tssv)
        theta_symbol.next_to(arc, RIGHT, tssv / 2)
        theta_symbol.shift(tssv * SMALL_BUFF * UP)

        return VGroup(wedge, arc, theta_symbol)

    def get_groups(self, theta):
        group = self.get_group(theta)
        angles = [k * theta for k in range(int(PI / theta) + 1)]
        groups = VGroup(*[
            group.copy().rotate(angle, about_point=ORIGIN)
            for angle in angles
        ])
        # colors = it.cycle([BLUE_D, BLUE_B, BLUE_C, GREY_BROWN])
        colors = it.cycle([BLUE_D, GREY_BROWN])
        for n, angle, group, color in zip(it.count(1), angles, groups, colors):
            wedge, arc, symbol = group
            symbol.rotate(-angle)
            arc.set_color(color)
            number = Integer(n)
            number.set_height(self.number_height)
            number.move_to(center_of_mass([
                wedge[0].get_end(),
                wedge[1].get_end(),
            ]))
            group.add(number)
        groups[-1][-1].set_color(RED)

        return groups

    def get_horizon(self):
        horizon = DashedLine(5 * LEFT, 5 * RIGHT)
        horizon.set_stroke(WHITE, 1)
        return horizon

    def get_semicircle(self):
        return Arc(
            start_angle=0,
            angle=PI,
            radius=self.wedge_radius / 2,
            color=YELLOW,
            stroke_width=4,
        )

    def get_inequality(self):
        ineq = OldTex(
            "N", "\\cdot", "\\theta", "<",
            "\\pi", "=", "3.1415926\\dots"
        )
        N = ineq.get_part_by_tex("N")
        self.pi_symbol = ineq.get_part_by_tex("\\pi")
        N.set_color(YELLOW)
        # ineq[-3:].set_color(BLUE)

        brace = Brace(N, UP, buff=SMALL_BUFF)
        text = brace.get_text("Maximum", buff=SMALL_BUFF)
        group = VGroup(ineq, brace, text)
        group.next_to(ORIGIN, DOWN, MED_LARGE_BUFF)
        return group

    def get_dynamic_inequality(self, counter):
        multiple = Integer(0)
        dot = OldTex("\\cdot")
        theta_tex = OldTex("({:.2f})".format(self.theta))
        eq = OldTex("=")
        value = DecimalNumber(0)
        ineq = OldTex("<")
        pi = OldTex("\\pi", "=", "3.1415926\\dots")
        # pi.set_color(BLUE)
        group = VGroup(
            multiple, dot, theta_tex,
            eq, value,
            ineq, pi
        )
        group.arrange(RIGHT, buff=0.2)
        group.next_to(ORIGIN, DOWN, buff=LARGE_BUFF)
        theta_brace = Brace(group[2], DOWN, buff=SMALL_BUFF)
        theta_symbol = theta_brace.get_tex("\\theta")
        group.add(theta_brace, theta_symbol)
        # group.align_to(self.pi_symbol, RIGHT)

        def get_count():
            return int(counter.get_value())

        def get_product():
            return get_count() * self.theta

        def is_greater_than_pi():
            return get_product() > PI

        def get_color():
            return RED if is_greater_than_pi() else YELLOW

        def get_ineq():
            result = OldTex(
                ">" if is_greater_than_pi() else "<"
            )
            result.set_color(get_color())
            result.move_to(ineq)
            return result
        dynamic_ineq = always_redraw(get_ineq)
        group.remove(ineq)
        group.add(dynamic_ineq)

        multiple.add_updater(lambda m: m.set_value(get_count()))
        multiple.add_updater(lambda m: m.next_to(dot, LEFT, 0.2))
        multiple.add_updater(lambda m: m.set_color(get_color()))
        value.add_updater(lambda m: m.set_value(get_product()))

        return group


class AskAboutAddingThetaToItselfThetaPoint2(AskAboutAddingThetaToItself):
    CONFIG = {
        "theta": 0.2,
        "wait_time": 0.1,
    }
