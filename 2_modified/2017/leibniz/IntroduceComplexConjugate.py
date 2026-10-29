# ==============================================================================
# Scene:      IntroduceComplexConjugate
# Source:     videos/_2017/leibniz.py (lines 1345-1715)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceComplexConjugate.py IntroduceComplexConjugate -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - add_background_rectangle leaves [rect, parts...] in GL (Cairo nested the tex one level down): index the parts directly
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


class IntroduceComplexConjugate(LatticePointScene):
    CONFIG = {
        "y_radius" : 20,
        "x_radius" : 30,
        "plane_scale_factor" : 1.7,
        "plane_center" : 2*LEFT,
        "example_coords" : (3, 4),
        "x_color" : GREEN,
        "y_color" : RED,
    }
    def construct(self):
        self.resize_plane()
        self.write_points_with_complex_coords()
        self.introduce_complex_conjugate()
        self.show_confusion()
        self.expand_algebraically()
        self.discuss_geometry()
        self.show_geometrically()

    def resize_plane(self):
        self.plane.scale(
            self.plane_scale_factor,
            about_point = self.plane_center
        )
        self.plane.set_stroke(width = 1)
        self.plane.axes.set_stroke(width = 3)

    def write_points_with_complex_coords(self):
        x, y = self.example_coords
        x_color = self.x_color
        y_color = self.y_color

        point = self.plane.coords_to_point(x, y)
        dot = Dot(point, color = self.dot_color)
        x_point = self.plane.coords_to_point(x, 0)
        h_arrow = Arrow(self.plane_center, x_point, buff = 0)
        v_arrow = Arrow(x_point, point, buff = 0)
        h_arrow.set_color(x_color)
        v_arrow.set_color(y_color)
        x_coord = OldTex(str(x))
        x_coord.next_to(h_arrow, DOWN, SMALL_BUFF)
        x_coord.set_color(x_color)
        x_coord.add_background_rectangle()
        y_coord = OldTex(str(y))
        imag_y_coord = OldTex(str(y) + "i")
        for coord in y_coord, imag_y_coord:
            coord.next_to(v_arrow, RIGHT, SMALL_BUFF)
            coord.set_color(y_color)
            coord.add_background_rectangle()

        tuple_label = OldTex(str((x, y)))
        tuple_label[1].set_color(x_color)
        tuple_label[3].set_color(y_color)
        complex_label = OldTex("%d+%di"%(x, y))
        complex_label[0].set_color(x_color)
        complex_label[2].set_color(y_color)
        for label in tuple_label, complex_label:
            label.add_background_rectangle()
            label.next_to(dot, UP+RIGHT, buff = 0)

        y_range = list(range(-9, 10, 3))
        ticks = VGroup(*[
            Line(
                ORIGIN, MED_SMALL_BUFF*RIGHT
            ).move_to(self.plane.coords_to_point(0, y))
            for y in y_range
        ])
        imag_coords = VGroup()
        for y, tick in zip(y_range, ticks):
            if y == 0:
                continue
            if y == 1:
                tex = "i"
            elif y == -1:
                tex = "-i"
            else:
                tex = "%di"%y
            imag_coord = OldTex(tex)
            imag_coord.scale(0.75)
            imag_coord.add_background_rectangle()
            imag_coord.next_to(tick, LEFT, SMALL_BUFF)
            imag_coords.add(imag_coord)

        self.add(dot)
        self.play(
            ShowCreation(h_arrow),
            Write(x_coord)
        )
        self.play(
            ShowCreation(v_arrow),
            Write(y_coord)
        )
        self.play(FadeIn(tuple_label))
        self.wait()
        self.play(*list(map(FadeOut, [tuple_label, y_coord])))
        self.play(*list(map(FadeIn, [complex_label, imag_y_coord])))
        self.play(*list(map(Write, [imag_coords, ticks])))
        self.wait()
        self.play(*list(map(FadeOut, [
            v_arrow, h_arrow, 
            x_coord, imag_y_coord,
        ])))

        self.complex_label = complex_label
        self.example_dot = dot

    def introduce_complex_conjugate(self):
        x, y = self.example_coords
        equation = VGroup(
            OldTex("25 = ", str(x), "^2", "+", str(y), "^2", "="),
            OldTex("(", str(x), "+", str(y), "i", ")"),
            OldTex("(", str(x), "-", str(y), "i", ")"),
        )
        equation.arrange(
            RIGHT, buff = SMALL_BUFF,
        )
        VGroup(*equation[-2:]).shift(0.5*SMALL_BUFF*DOWN)
        equation.scale(0.9)
        equation.to_corner(UP+RIGHT, buff = MED_SMALL_BUFF)
        equation.shift(MED_LARGE_BUFF*DOWN)
        for tex_mob in equation:
            tex_mob.set_color_by_tex(str(x), self.x_color)
            tex_mob.set_color_by_tex(str(y), self.y_color)
            tex_mob.add_background_rectangle()

        dot = Dot(
            self.plane.coords_to_point(x, -y),
            color = self.dot_color
        )
        label = OldTex("%d-%di"%(x, y))
        label[0].set_color(self.x_color)
        label[2].set_color(self.y_color)
        label.add_background_rectangle()
        label.next_to(dot, DOWN+RIGHT, buff = 0)

        brace = Brace(equation[-1], DOWN)
        conjugate_words = OldTexText("Complex \\\\ conjugate")
        conjugate_words.scale(0.8)
        conjugate_words.add_background_rectangle()
        conjugate_words.next_to(brace, DOWN)

        self.play(FadeIn(
            equation,
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait(2)
        self.play(
            GrowFromCenter(brace),
            Write(conjugate_words, run_time = 2)
        )
        self.wait()
        self.play(*[
            ReplacementTransform(m1.copy(), m2)
            for m1, m2 in [
                (self.example_dot, dot),
                (self.complex_label, label),
            ]
        ])
        self.wait(2)

        self.conjugate_label = VGroup(brace, conjugate_words)
        self.equation = equation
        self.conjugate_dot = dot

    def show_confusion(self):
        randy = Randolph(color = BLUE_C).to_corner(DOWN+LEFT)
        morty = Mortimer().to_edge(DOWN)
        randy.make_eye_contact(morty)

        self.play(*list(map(FadeIn, [randy, morty])))
        self.play(PiCreatureSays(
            randy, "Wait \\dots why?",
            target_mode = "confused",
        ))
        self.play(Blink(randy))
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(
                randy, target_mode = "erm",
            ),
            PiCreatureSays(
                morty, "Now it's a \\\\ factoring problem!",
                target_mode = "hooray",
                bubble_config = {"width" : 5, "height" : 3}
            )
        )
        self.play(
            morty.look_at, self.equation,
            randy.look_at, self.equation,
        )
        self.play(Blink(morty))
        self.play(randy.change_mode, "pondering")
        self.play(RemovePiCreatureBubble(morty))
        self.play(*list(map(FadeOut, [randy, morty])))

    def expand_algebraically(self):
        x, y = self.example_coords
        expansion = VGroup(
            OldTex(str(x), "^2"),
            OldTex("-", "(", str(y), "i", ")^2")
        )
        expansion.arrange(RIGHT, buff = SMALL_BUFF)
        expansion.next_to(
            VGroup(*self.equation[-2:]), 
            DOWN, LARGE_BUFF
        )
        alt_y_term = OldTex("+", str(y), "^2")
        alt_y_term.move_to(expansion[1], LEFT)
        for tex_mob in list(expansion) + [alt_y_term]:
            tex_mob.set_color_by_tex(str(x), self.x_color)
            tex_mob.set_color_by_tex(str(y), self.y_color)
            tex_mob.rect = BackgroundRectangle(tex_mob)

        # CHANGE: add_background_rectangle leaves [rect, parts...] in GL (Cairo nested the tex one level down): index the parts directly
        x1 = self.equation[-2][2]
        x2 = self.equation[-1][2]
        y1 = VGroup(*self.equation[-2][4:6])
        y2 = VGroup(*self.equation[-1][3:6])
        vect = MED_LARGE_BUFF*UP

        self.play(FadeOut(self.conjugate_label))
        group = VGroup(x1, x2)
        self.play(group.shift, -vect)
        self.play(
            FadeIn(expansion[0].rect),
            ReplacementTransform(group.copy(), expansion[0]),
        )
        self.play(group.shift, vect)
        group = VGroup(x1, y2)
        self.play(group.shift, -vect)
        self.wait()
        self.play(group.shift, vect)
        group = VGroup(x2, y1)
        self.play(group.shift, -vect)
        self.wait()
        self.play(group.shift, vect)
        group = VGroup(*it.chain(y1, y2))
        self.play(group.shift, -vect)
        self.wait()
        self.play(
            FadeIn(expansion[1].rect),
            ReplacementTransform(group.copy(), expansion[1]),
        )
        self.play(group.shift, vect)
        self.wait(2)
        self.play(
            Transform(expansion[1].rect, alt_y_term.rect),
            Transform(expansion[1], alt_y_term),
        )
        self.wait()
        self.play(*list(map(FadeOut, [
            expansion[0].rect,
            expansion[1].rect,
            expansion
        ])))

    def discuss_geometry(self):
        randy = Randolph(color = BLUE_C)
        randy.scale(0.8)
        randy.to_corner(DOWN+LEFT)
        morty = Mortimer()
        morty.set_height(randy.get_height())
        morty.next_to(randy, RIGHT)
        randy.make_eye_contact(morty)
        screen = ScreenRectangle(height = 3.5)
        screen.to_corner(DOWN+RIGHT, buff = MED_SMALL_BUFF)

        self.play(*list(map(FadeIn, [randy, morty])))
        self.play(PiCreatureSays(
            morty, "More geometry!",
            target_mode = "hooray",
            run_time = 2,
            bubble_config = {"height" : 2, "width" : 4}
        ))
        self.play(Blink(randy))
        self.play(
            RemovePiCreatureBubble(
                morty, target_mode = "plain",
            ),
            PiCreatureSays(
                randy, "???",
                target_mode = "maybe",
                bubble_config = {"width" : 3, "height" : 2}
            )
        )
        self.play(
            ShowCreation(screen),
            morty.look_at, screen,
            randy.look_at, screen,
        )
        self.play(Blink(morty))
        self.play(RemovePiCreatureBubble(randy, target_mode = "pondering"))
        self.wait()
        self.play(*list(map(FadeOut, [randy, morty, screen])))

    def show_geometrically(self):
        dots = [self.example_dot, self.conjugate_dot]
        top_dot, low_dot = dots
        for dot in dots:
            dot.line = Line(
                self.plane_center, dot.get_center(), 
                color = BLUE
            )
            dot.angle = dot.line.get_angle()
            dot.arc = Arc(
                dot.angle,
                radius = 0.75, 
                color = YELLOW
            )
            dot.arc.shift(self.plane_center)
            dot.arc.add_tip(tip_length = 0.2)
            dot.rotate_word = OldTexText("Rotate")
            dot.rotate_word.scale(0.5)
            dot.rotate_word.next_to(dot.arc, RIGHT, SMALL_BUFF)
            dot.magnitude_word = OldTexText("Length 5")
            dot.magnitude_word.scale(0.6)
            dot.magnitude_word.next_to(
                ORIGIN,
                np.sign(dot.get_center()[1])*UP,
                buff = SMALL_BUFF
            )
            dot.magnitude_word.add_background_rectangle()
            dot.magnitude_word.rotate(dot.angle)
            dot.magnitude_word.shift(dot.line.get_center())
        twenty_five_label = OldTex("25")
        twenty_five_label.add_background_rectangle()
        twenty_five_label.next_to(
            self.plane.coords_to_point(25, 0),
            DOWN
        )

        self.play(ShowCreation(top_dot.line))
        mover = VGroup(
            top_dot.line.copy().set_color(PINK), 
            top_dot.copy()
        )
        self.play(FadeIn(
            top_dot.magnitude_word,
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(ShowCreation(top_dot.arc))
        self.wait(2)
        self.play(ShowCreation(low_dot.line))
        self.play(
            ReplacementTransform(
                top_dot.arc,
                low_dot.arc
            ),
            FadeIn(low_dot.rotate_word)
        )
        self.play(
            Rotate(
                mover, low_dot.angle, 
                about_point = self.plane_center
            ),
            run_time = 2
        )
        self.play(
            FadeOut(low_dot.arc),
            FadeOut(low_dot.rotate_word),
            FadeIn(low_dot.magnitude_word),
        )
        self.play(
            mover[0].scale_about_point, 5, self.plane_center,
            mover[1].move_to, self.plane.coords_to_point(25, 0),
            run_time = 2
        )
        self.wait()
        self.play(Write(twenty_five_label))
        self.wait(3)
