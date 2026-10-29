# ==============================================================================
# Scene:      AddCircleSymmetries
# Source:     videos/_2017/efvgt.py (lines 867-942)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AddCircleSymmetries.py AddCircleSymmetries -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Circle.radius is a read-only float property: keep the radius Line under another name
#   - GL Circle.radius is a read-only float property: use the saved radius Line
#   - Transform(a, b).update(1) in an updater leaks time and memory in this fork (BUGS_FORK_2018 #4): become() gives the same end state
# ==============================================================================

from manim_imports_ext import *

class CircleSymmetries(Scene):
    CONFIG = {
        "circle_radius" : 2,
    }
    def construct(self):
        self.add_circle_and_title()        
        self.show_range_of_angles()
        self.associate_rotations_with_points()

    def add_circle_and_title(self):
        title = OldTexText("Group of rotations")
        title.to_edge(UP)

        circle = self.get_circle()

        self.play(Write(title), ShowCreation(circle, run_time = 2))
        self.wait()
        angles = [
            np.pi/2, -np.pi/3, 5*np.pi/6, 
            3*np.pi/2 + 0.1
        ]
        angles.append(-sum(angles))
        for angle in angles:
            self.play(Rotate(circle, angle = angle))
            self.wait()

        self.circle = circle

    def show_range_of_angles(self):
        self.add_radial_line()
        arc_circle = self.get_arc_circle()

        theta = OldTex("\\theta = ")
        theta_value = DecimalNumber(0.00)
        theta_value.next_to(theta, RIGHT)
        theta_group = VGroup(theta, theta_value)
        theta_group.next_to(arc_circle, UP)
        def theta_value_update(theta_value, alpha):
            new_theta_value = DecimalNumber(alpha*2*np.pi)
            new_theta_value.set_height(theta.get_height())
            new_theta_value.next_to(theta, RIGHT)
            # CHANGE: Transform(a, b).update(1) in an updater leaks time and memory in this fork (BUGS_FORK_2018 #4): become() gives the same end state
            theta_value.become(new_theta_value)
            return new_theta_value


        self.play(FadeIn(theta_group))
        for rate_func in smooth, lambda t : smooth(1-t):
            self.play(
                Rotate(self.circle, 2*np.pi-0.001),
                ShowCreation(arc_circle),
                UpdateFromAlphaFunc(theta_value, theta_value_update),
                run_time = 7,
                rate_func = rate_func
            )
            self.wait()
        self.play(FadeOut(theta_group))
        self.wait()

    def associate_rotations_with_points(self):
        zero_dot = Dot(self.circle.point_from_proportion(0))
        zero_dot.set_color(RED)
        zero_arrow = Arrow(UP+RIGHT, ORIGIN)
        zero_arrow.set_color(zero_dot.get_color())
        zero_arrow.next_to(zero_dot, UP+RIGHT, buff = SMALL_BUFF)

        self.play(
            ShowCreation(zero_arrow),
            DrawBorderThenFill(zero_dot)
        )
        self.circle.add(zero_dot)
        self.wait()

        for alpha in 0.2, 0.6, 0.4, 0.8:
            point = self.circle.point_from_proportion(alpha)
            dot = Dot(point, color = YELLOW)
            vect = np.sign(point)
            arrow = Arrow(vect, ORIGIN)
            arrow.next_to(dot, vect, buff = SMALL_BUFF)
            arrow.set_color(dot.get_color())
            angle = alpha*2*np.pi

            self.play(
                ShowCreation(arrow),
                DrawBorderThenFill(dot)
            )
            self.play(
                Rotate(self.circle, angle, run_time = 2),
                Animation(dot)
            )
            self.wait()            
            self.play(
                Rotate(self.circle, -angle, run_time = 2),
                FadeOut(dot),
                FadeOut(arrow),
            )
            self.wait()

    ####

    def get_circle(self):
        circle = Circle(color = MAROON_B, radius = self.circle_radius)
        circle.ticks = VGroup()
        for alpha in np.arange(0, 1, 1./8):
            point = circle.point_from_proportion(alpha)
            tick = Line((1 - 0.05)*point, (1 + 0.05)*point)
            circle.ticks.add(tick)
        circle.add(circle.ticks)
        return circle

    def add_radial_line(self):
        radius = Line(
            self.circle.get_center(), 
            self.circle.point_from_proportion(0)
        )
        static_radius = radius.copy().set_color(GREY)

        self.play(ShowCreation(radius))
        self.add(static_radius, radius)
        # CHANGE: GL Circle.radius is a read-only float property: keep the radius Line under another name
        self.circle.radius_line = radius
        self.circle.static_radius = static_radius
        self.circle.add(radius)

    def get_arc_circle(self):
        arc_radius = self.circle_radius/5.0
        arc_circle = Circle(
            radius = arc_radius,
            color = WHITE
        )
        return arc_circle


class AddCircleSymmetries(CircleSymmetries):
    def construct(self):
        circle = self.circle = self.get_circle()
        arc_circle = self.get_arc_circle()
        angles = [3*np.pi/2, 2*np.pi/3, np.pi/6]
        arcs = [
            arc_circle.copy().scale(scalar)
            for scalar in [1, 1.2, 1.4]
        ]

        equation = OldTex(
            "270^\\circ", "+", "120^\\circ", "=", "30^\\circ",
        )
        equation.to_edge(UP)

        colors = [BLUE, YELLOW, GREEN]
        for color, arc, term in zip(colors, arcs, equation[::2]):
            arc.set_color(color)
            term.set_color(color)

        self.play(FadeIn(circle))
        self.add_radial_line()
        # CHANGE: GL Circle.radius is a read-only float property: use the saved radius Line
        alt_radius = circle.radius_line.copy()
        alt_radius.set_color(GREY)
        alt_circle = circle.copy()
        equals = OldTex("=")
        equals.move_to(circle)

        def rotate(circle, angle, arc, terms):
            self.play(
                Rotate(circle, angle, in_place = True),
                ShowCreation(
                    arc,
                    rate_func = lambda t : (angle/(2*np.pi))*smooth(t)
                ),
                Write(VGroup(*terms)),
                run_time = 2,
            )

        rotate(circle, angles[0], arcs[0], equation[:2])
        self.wait()
        circle.add(alt_radius)
        rotate(circle, angles[1], arcs[1], equation[2:4])
        self.play(FadeOut(alt_radius))
        circle.remove(alt_radius)
        self.wait()

        circle.add(circle.static_radius)
        circle.add(*arcs[:2])

        alt_static_radius = circle.static_radius.copy()
        alt_circle.add(alt_static_radius)
        alt_circle.next_to(equals, RIGHT, buff = LARGE_BUFF)
        alt_circle.save_state()
        alt_circle.move_to(circle)
        alt_circle.set_stroke(width = 0)
        self.play(
            circle.next_to, equals, LEFT, LARGE_BUFF,
            alt_circle.restore,
            Write(equals)
        )
        arcs[2].shift(alt_circle.get_center())
        alt_circle.remove(alt_static_radius)
        self.wait()
        rotate(alt_circle, angles[2], arcs[2], equation[4:])
        self.wait()
        self.play(
            Rotate(arcs[1], angles[0], about_point = circle.get_center())
        )
        self.wait(2)
        for term, arc in zip(equation[::2], arcs):
            self.play(*[
                ApplyMethod(mob.scale, 1.2, rate_func = there_and_back)
                for mob in (term, arc)
            ])
            self.wait()
