# ==============================================================================
# Scene:      TrigIdentity
# Source:     videos/_2021/some1.py (lines 175-255)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TrigIdentity.py TrigIdentity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TrigIdentity(Scene):
    def construct(self):
        plane = NumberPlane().scale(2)
        circle = Circle(radius=2)
        circle.set_stroke(YELLOW, 2)

        theta_tracker = ValueTracker(60 * DEGREES)
        get_theta = theta_tracker.get_value

        def get_point():
            return circle.pfp(get_theta() / TAU)

        dot = Dot()
        f_always(dot.move_to, get_point)
        radial_line = always_redraw(lambda: Line(plane.c2p(0, 0), get_point()))
        tan_line = always_redraw(
            lambda: Line(get_point(), plane.c2p(1 / math.cos(get_theta()), 0), stroke_color=RED)
        )
        sec_line = always_redraw(
            lambda: Line(plane.c2p(0, 0), tan_line.get_end(), stroke_color=PINK)
        )

        def get_one_label():
            one = Integer(1)
            one.next_to(radial_line.get_center(), UL, SMALL_BUFF)
            return one

        def get_tan_label():
            label = OldTex("\\tan(\\theta)")
            label.set_color(RED)
            point = tan_line.get_center()
            label.next_to(point, UP, SMALL_BUFF)
            label.rotate(tan_line.get_angle(), about_point=point)
            label.set_stroke(BLACK, 3, background=True)
            return label

        def get_sec_label():
            label = OldTex("\\sec(\\theta)")
            label.set_color(PINK)
            label.next_to(sec_line, DOWN, SMALL_BUFF)
            label.set_stroke(BLACK, 3, background=True)
            return label

        one_label = always_redraw(get_one_label)
        tan_label = always_redraw(get_tan_label)
        sec_label = always_redraw(get_sec_label)

        arc = always_redraw(lambda: Arc(0, get_theta(), radius=0.25))
        arc_label = OldTex("\\theta", font_size=36)
        arc_label.next_to(arc, RIGHT, SMALL_BUFF, DOWN).shift(SMALL_BUFF * UP)

        equation = OldTex(
            "\\tan^2(\\theta) + 1 = \\sec^2(\\theta)",
            tex_to_color_map={
                "\\tan": RED,
                "\\sec": PINK,
            },
            font_size=60
        )
        equation.to_corner(UL)
        equation.set_stroke(BLACK, 7, background=True)

        self.add(plane)
        self.add(circle)
        self.add(equation)

        self.add(radial_line)
        self.add(tan_line)
        self.add(sec_line)
        self.add(dot)

        self.add(one_label)
        self.add(tan_label)
        self.add(sec_label)

        self.add(arc)
        self.add(arc_label)

        angles = [40 * DEGREES, 70 * DEGREES]
        for angle in angles:
            self.play(theta_tracker.animate.set_value(angle), run_time=4)
