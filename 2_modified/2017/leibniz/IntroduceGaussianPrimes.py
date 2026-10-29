# ==============================================================================
# Scene:      IntroduceGaussianPrimes
# Source:     videos/_2017/leibniz.py (lines 1941-2122)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceGaussianPrimes.py IntroduceGaussianPrimes -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL InteractiveScene.setup (via PiCreatureScene) must run before the first self.add
# ==============================================================================

from manim_imports_ext import *

class LatticePointScene(Scene):
    CONFIG = {
        "y_radius" : 6,
        "x_radius" : None,
        "plane_center" : ORIGIN,
        "max_lattice_point_radius" : 6,
        "dot_radius" : 0.075,
        "secondary_line_ratio" : 0,
        "plane_color" : BLUE_E,
        "dot_color" : YELLOW,
        "dot_drawing_stroke_color" : PINK,
        "circle_color" : MAROON_D,
        "radial_line_color" : RED,
    }
    def setup(self):
        if self.x_radius is None:
            self.x_radius = self.y_radius*FRAME_X_RADIUS/FRAME_Y_RADIUS
        plane = ComplexPlane(
            y_radius = self.y_radius,
            x_radius = self.x_radius,
            secondary_line_ratio = self.secondary_line_ratio,
            radius = self.plane_color
        )
        plane.set_height(FRAME_HEIGHT)
        plane.shift(self.plane_center)
        self.add(plane)
        self.plane = plane

        self.setup_lattice_points()

    def setup_lattice_points(self):
        M = self.max_lattice_point_radius
        int_range = list(range(-M, M+1))
        self.lattice_points = VGroup()
        for x, y in it.product(*[int_range]*2):
            r_squared = x**2 + y**2
            if r_squared > M**2:
                continue
            dot = Dot(
                self.plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            dot.r_squared = r_squared
            self.lattice_points.add(dot)
        self.lattice_points.sort(
            lambda p : get_norm(p - self.plane_center)
        )

    def get_circle(self, radius = None, color = None):
        if radius is None:
            radius = self.max_lattice_point_radius
        if color is None:
            color = self.circle_color
        radius *= self.plane.get_space_unit_to_y_unit()
        circle = Circle(
            color = color,
            radius = radius,
        )
        circle.move_to(self.plane.get_center())
        return circle

    def get_radial_line_with_label(self, radius = None, color = None):
        if radius is None:
            radius = self.max_lattice_point_radius
        if color is None:
            color = self.radial_line_color
        radial_line = Line(
            self.plane_center,
            self.plane.coords_to_point(radius, 0),
            color = color
        )
        r_squared = int(np.round(radius**2))
        root_label = OldTex("\\sqrt{%d}"%r_squared)
        root_label.add_background_rectangle()
        root_label.next_to(radial_line, UP, SMALL_BUFF)

        return radial_line, root_label

    def get_lattice_points_on_r_squared_circle(self, r_squared):
        points = VGroup(*[dot for dot in self.lattice_points if dot.r_squared == r_squared])
        points.sort(
            lambda p : angle_of_vector(p-self.plane_center)%(2*np.pi)
        )
        return points

    def draw_lattice_points(self, points = None, run_time = 4):
        if points is None:
            points = self.lattice_points
        self.play(*[
            DrawBorderThenFill(
                dot,
                stroke_width = 4,
                stroke_color = self.dot_drawing_stroke_color,
                run_time = run_time,
                rate_func = squish_rate_func(
                    double_smooth, a, a + 0.25
                ),
            )
            for dot, a in zip(
                points, 
                np.linspace(0, 0.75, len(points))
            )
        ])

    def add_axis_labels(self, spacing = 2):
        x_max = int(self.plane.point_to_coords(FRAME_X_RADIUS*RIGHT)[0])
        y_max = int(self.plane.point_to_coords(FRAME_Y_RADIUS*UP)[1])
        x_range = list(range(spacing, x_max, spacing))
        y_range = list(range(spacing, y_max, spacing))
        for r in x_range, y_range:
            r += [-n for n in r]
        tick = Line(ORIGIN, MED_SMALL_BUFF*UP)
        x_ticks = VGroup(*[
            tick.copy().move_to(self.plane.coords_to_point(x, 0))
            for x in x_range
        ])
        tick.rotate(-np.pi/2)
        y_ticks = VGroup(*[
            tick.copy().move_to(self.plane.coords_to_point(0, y))
            for y in y_range
        ])
        x_labels = VGroup(*[
            OldTex(str(x))
            for x in x_range
        ])
        y_labels = VGroup(*[
            OldTex(str(y) + "i")
            for y in y_range
        ])

        for labels, ticks in (x_labels, x_ticks), (y_labels, y_ticks):
            labels.scale(0.6)
            for tex_mob, tick in zip(labels, ticks):
                tex_mob.add_background_rectangle()
                tex_mob.next_to(
                    tick,
                    tick.get_start() - tick.get_end(),
                    SMALL_BUFF
                )
        self.add(x_ticks, y_ticks, x_labels, y_labels)
        digest_locals(self, [
            "x_ticks", "y_ticks",
            "x_labels", "y_labels",
        ])

    def point_to_int_coords(self, point):
        x, y = self.plane.point_to_coords(point)[:2]
        return (int(np.round(x)), int(np.round(y)))

    def dot_to_int_coords(self, dot):
        return self.point_to_int_coords(dot.get_center())


class IntroduceGaussianPrimes(LatticePointScene, PiCreatureScene):
    CONFIG = {
        "plane_center" : LEFT,
        "x_radius" : 13,
    }
    def create_pi_creature(self):
        morty = Mortimer().flip()
        morty.scale(0.7)
        morty.next_to(ORIGIN, UP, buff = 0)
        morty.to_edge(LEFT)
        return morty

    def setup(self):
        # CHANGE: GL InteractiveScene.setup (via PiCreatureScene) must run before the first self.add
        PiCreatureScene.setup(self)
        LatticePointScene.setup(self)
        self.remove(self.pi_creature)

    def construct(self):
        self.plane.set_stroke(width = 2)
        morty = self.pi_creature
        dots = [
            Dot(self.plane.coords_to_point(*coords))
            for coords in [
                (5, 0), 
                (2, 1), (2, -1), 
                (-1, 2), (-1, -2),
                (-2, -1), (-2, 1),
            ]
        ]
        five_dot = dots[0]
        five_dot.set_color(YELLOW)
        p_dots = VGroup(*dots[1:])
        p1_dot, p2_dot, p3_dot, p4_dot, p5_dot, p6_dot = p_dots
        VGroup(p1_dot, p3_dot, p5_dot).set_color(PINK)
        VGroup(p2_dot, p4_dot, p6_dot).set_color(RED)

        labels = [
            OldTex(tex).add_background_rectangle()
            for tex in ("5", "2+i", "2-i", "-1+2i", "-1-2i", "-2-i", "-2+i")
        ]
        five_label, p1_label, p2_label, p3_label, p4_label, p5_label, p6_label = labels
        vects = [
            DOWN, 
            UP+RIGHT, DOWN+RIGHT, 
            UP+LEFT, DOWN+LEFT,
            DOWN+LEFT, UP+LEFT,
        ]
        for dot, label, vect in zip(dots, labels, vects):
            label.next_to(dot, vect, SMALL_BUFF)

        arc_angle = 0.8*np.pi
        times_i_arc = Arrow(
            p1_dot.get_top(), p3_dot.get_top(), 
            path_arc = arc_angle
        )
        times_neg_i_arc = Arrow(
            p2_dot.get_bottom(), p4_dot.get_bottom(), 
            path_arc = -arc_angle
        )
        times_i = OldTex("\\times i")
        times_i.add_background_rectangle()
        times_i.next_to(
            times_i_arc.point_from_proportion(0.5),
            UP
        )
        times_neg_i = OldTex("\\times (-i)")
        times_neg_i.add_background_rectangle()
        times_neg_i.next_to(
            times_neg_i_arc.point_from_proportion(0.5),
            DOWN
        )
        VGroup(
            times_i, times_neg_i, times_i_arc, times_neg_i_arc
        ).set_color(MAROON_B)

        gaussian_prime = OldTexText("$\\Rightarrow$ ``Gaussian prime''")
        gaussian_prime.add_background_rectangle()
        gaussian_prime.scale(0.9)
        gaussian_prime.next_to(p1_label, RIGHT)

        factorization = OldTex(
            "5", "= (2+i)(2-i)"
        )
        factorization.to_corner(UP+RIGHT)
        factorization.shift(1.5*LEFT)
        factorization.add_background_rectangle()
        neg_alt_factorization = OldTex("=(-2-i)(-2+i)")
        i_alt_factorization = OldTex("=(-1+2i)(-1-2i)")
        for alt_factorization in neg_alt_factorization, i_alt_factorization:
            alt_factorization.next_to(
                factorization.get_part_by_tex("="), DOWN,
                aligned_edge = LEFT
            )
            alt_factorization.add_background_rectangle()

        for dot in dots:
            dot.add(Line(
                self.plane_center,
                dot.get_center(),
                color = dot.get_color()
            ))

        self.add(factorization)
        self.play(
            DrawBorderThenFill(five_dot), 
            FadeIn(five_label)
        )
        self.wait()
        self.play(
            ReplacementTransform(
                VGroup(five_dot).copy(),
                VGroup(p1_dot, p2_dot)
            )
        )
        self.play(*list(map(Write, [p1_label, p2_label])))
        self.wait()
        self.play(Write(gaussian_prime))
        self.wait()

        #Show morty
        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "\\emph{Almost} unique",
            bubble_config = {"height" : 2, "width" : 5},
        ))
        self.wait()
        self.play(RemovePiCreatureBubble(morty, target_mode = "pondering"))

        #Show neg_alternate expression 
        movers = [p1_dot, p2_dot, p1_label, p2_label]
        for mover in movers:
            mover.save_state()
        self.play(
            Transform(p1_dot, p5_dot),
            Transform(p1_label, p5_label),
        )
        self.play(
            Transform(p2_dot, p6_dot),
            Transform(p2_label, p6_label),
        )
        self.play(Write(neg_alt_factorization))
        self.wait()
        self.play(
            FadeOut(neg_alt_factorization),
            *[m.restore for m in movers]
        )
        self.wait()

        ##Show i_alternate expression
        self.play(
            ShowCreation(times_i_arc),
            FadeIn(times_i),
            *[
                ReplacementTransform(
                    mob1.copy(), mob2,
                    path_arc = np.pi/2
                )
                for mob1, mob2 in [
                    (p1_dot, p3_dot),
                    (p1_label, p3_label),
                ]
            ]
        )
        self.wait()
        self.play(
            ShowCreation(times_neg_i_arc),
            FadeIn(times_neg_i),
            *[
                ReplacementTransform(
                    mob1.copy(), mob2,
                    path_arc = -np.pi/2
                )
                for mob1, mob2 in [
                    (p2_dot, p4_dot),
                    (p2_label, p4_label),
                ]
            ]
        )
        self.wait()
        self.play(Write(i_alt_factorization))
        self.change_mode("hesitant")
        self.wait(3)
