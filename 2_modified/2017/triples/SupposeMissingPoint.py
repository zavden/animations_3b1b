# ==============================================================================
# Scene:      SupposeMissingPoint
# Source:     videos/_2017/triples.py (lines 2488-2567)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SupposeMissingPoint.py SupposeMissingPoint -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - complex_string is not importable here: str(z) without the parentheses (what the 3feb helper returned)
#   - typo in the original (color_grids is undefined, NameError also in Cairo)
#   - typo in the original (background_planes is never defined; NameError also in Cairo)
# ==============================================================================

from manim_imports_ext import *

def complex_string_with_i(z):
    if z.real == 0:
        return str(int(z.imag)) + "i"
    elif z.imag == 0:
        return str(int(z.real))
    # CHANGE: complex_string is not importable here: str(z) without the parentheses (what the 3feb helper returned)
    return "".join(c for c in str(z) if c not in "()").replace("j", "i")


class VisualizeZSquared(Scene):
    CONFIG = {
        "initial_unit_size" : 0.4,
        "final_unit_size" : 0.1,
        "plane_center" : 3*LEFT + 2*DOWN,
        "x_label_range" : list(range(-12, 24, 4)),
        "y_label_range" : list(range(-4, 24, 4)),
        "dot_color" : YELLOW,
        "square_color" : MAROON_B,
        "big_dot_radius" : 0.075,
        "dot_radius" : 0.05,
    }
    def construct(self):
        self.force_skipping()

        self.add_plane()
        self.write_z_to_z_squared()
        self.draw_arrows()
        self.draw_dots()
        self.add_colored_grid()
        self.apply_transformation()
        self.show_triangles()
        self.zoom_out()
        self.show_more_triangles()

    def add_plane(self):
        width = (FRAME_X_RADIUS+abs(self.plane_center[0]))/self.final_unit_size
        height = (FRAME_Y_RADIUS+abs(self.plane_center[1]))/self.final_unit_size
        background_plane = ComplexPlane(
            x_radius = width,
            y_radius = height,
            stroke_width = 2,
            stroke_color = BLUE_E,
            secondary_line_ratio = 0,
        )
        background_plane.axes.set_stroke(width = 4)

        background_plane.scale(self.initial_unit_size)
        background_plane.shift(self.plane_center)

        coordinate_labels = VGroup()
        z_list = np.append(
            self.x_label_range,
            complex(0, 1)*np.array(self.y_label_range)
        )
        for z in z_list:
            if z == 0:
                continue
            if z.imag == 0:
                tex = str(int(z.real))
            else:
                tex = str(int(z.imag)) + "i"
            label = OldTex(tex)
            label.scale(0.75)
            label.add_background_rectangle()
            point = background_plane.number_to_point(z)
            if z.imag == 0:
                label.next_to(point, DOWN, SMALL_BUFF)
            else:
                label.next_to(point, LEFT, SMALL_BUFF)
            coordinate_labels.add(label)

        self.add(background_plane, coordinate_labels)
        self.background_plane = background_plane
        self.coordinate_labels = coordinate_labels

    def write_z_to_z_squared(self):
        z_to_z_squared = OldTex("z", "\\to", "z^2")
        z_to_z_squared.set_color_by_tex("z", YELLOW)
        z_to_z_squared.set_color_by_tex("z^2", MAROON_B)
        z_to_z_squared.add_background_rectangle()
        z_to_z_squared.to_edge(UP)
        z_to_z_squared.shift(2*RIGHT)

        self.play(Write(z_to_z_squared))
        self.wait()
        self.z_to_z_squared = z_to_z_squared

    def draw_arrows(self):
        z_list = [
            complex(2, 1),
            complex(3, 2),
            complex(0, 1),
            complex(-1, 0),
        ]

        arrows = VGroup()
        dots = VGroup()
        for z in z_list:
            z_point, square_point, mid_point = [
                self.background_plane.number_to_point(z**p)
                for p in (1, 2, 1.5)
            ]
            angle = Line(mid_point, square_point).get_angle()
            angle -= Line(z_point, mid_point).get_angle()
            angle *= 2
            arrow = Arrow(
                z_point, square_point, 
                path_arc = angle,
                color = WHITE,
                tip_length = 0.15,
                buff = SMALL_BUFF,
            )

            z_dot, square_dot = [
                Dot(
                    point, color = color,
                    radius = self.big_dot_radius,
                )
                for point, color in [
                    (z_point, self.dot_color),
                    (square_point, self.square_color),
                ]
            ]
            z_label = OldTex(complex_string_with_i(z))
            square_label = OldTex(complex_string_with_i(z**2))
            for label, point in (z_label, z_point), (square_label, square_point):
                if abs(z) > 2:
                    vect = RIGHT
                else:
                    vect = point - self.plane_center
                    vect /= get_norm(vect)
                    if abs(vect[1]) < 0.1:
                        vect[1] = -1
                label.next_to(point, vect)
                label.add_background_rectangle()

            self.play(*list(map(FadeIn, [z_label, z_dot])))
            self.wait()
            self.play(ShowCreation(arrow))
            self.play(ReplacementTransform(
                z_dot.copy(), square_dot,
                path_arc = angle
            ))
            self.play(FadeIn(square_label))
            self.wait()
            self.play(
                FadeOut(z_label),
                FadeOut(square_label),
                Animation(arrow)
            )

            arrows.add(arrow)
            dots.add(z_dot, square_dot)
        self.wait()
        self.play(*list(map(FadeOut, [
            dots, arrows, self.z_to_z_squared
        ])))

    def draw_dots(self):
        min_corner, max_corner = [
            self.background_plane.point_to_coords(
                u*FRAME_X_RADIUS*RIGHT + u*FRAME_Y_RADIUS*UP
            )
            for u in (-1, 1)
        ]
        x_min, y_min = list(map(int, min_corner[:2]))
        x_max, y_max = list(map(int, max_corner[:2]))

        dots = VGroup(*[
            Dot(
                self.background_plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            for x in range(x_min, x_max+1)
            for y in range(y_min, y_max+1)
        ])
        dots.sort(lambda p : np.dot(p, UP+RIGHT))

        self.add_foreground_mobject(self.coordinate_labels)
        self.play(LaggedStartMap(
            DrawBorderThenFill, dots,
            stroke_width = 3,
            stroke_color = PINK,
            run_time = 3,
            lag_ratio = 0.2
        ))
        self.wait()

        self.dots = dots

    def add_colored_grid(self):
        color_grid = self.get_color_grid()

        self.play(
            # CHANGE: typo in the original (background_planes is never defined; NameError also in Cairo)
            self.background_plane.set_stroke, None, 1,
            LaggedStartMap(
                FadeIn, color_grid, 
                run_time = 2
            ),
            Animation(self.dots),
        )
        self.wait()

        self.color_grid = color_grid

    def apply_transformation(self):
        for dot in self.dots:
            dot.start_point = dot.get_center()
        def update_dot(dot, alpha):
            event = list(dot.start_point) + [alpha]
            dot.move_to(self.homotopy(*event))
            return dot
        self.play(
            Homotopy(self.homotopy, self.color_grid),
            *[
                UpdateFromAlphaFunc(dot, update_dot)
                for dot in self.dots
            ],
            run_time = 3
        )
        self.wait(2)
        self.play(self.color_grid.set_stroke, None, 3)
        self.wait()
        scale_factor = self.big_dot_radius/self.dot_radius
        self.play(LaggedStartMap(
            ApplyMethod, self.dots,
            lambda d : (d.scale, scale_factor),
            rate_func = there_and_back,
            run_time = 3
        ))
        self.wait()

    def show_triangles(self):
        z_list = [
            complex(u, v)**2
            for u, v in [(2, 1), (3, 2), (4, 1)]
        ]
        triangles = self.get_triangles(z_list)
        triangle = triangles[0]
        triangle.save_state()
        triangle.scale(0.01, about_point = triangle.tip)

        self.play(triangle.restore, run_time = 2)
        self.wait(2)
        for new_triangle in triangles[1:]:
            self.play(Transform(triangle, new_triangle))
            self.wait(2)
        self.play(FadeOut(triangle))

    def zoom_out(self):
        self.remove_foreground_mobject(self.coordinate_labels)
        movers = [
            self.background_plane,
            self.color_grid,
            self.dots,
            self.coordinate_labels,
        ]
        scale_factor = self.final_unit_size/self.initial_unit_size
        for mover in movers:
            mover.generate_target()
            mover.target.scale(
                scale_factor,
                about_point = self.plane_center
            )
        for dot in self.dots.target:
            dot.scale(1./scale_factor)
        self.background_plane.target.fade()

        self.revert_to_original_skipping_status()
        self.play(
            *list(map(MoveToTarget, movers)),
            run_time = 3
        )
        self.wait(2)

    def show_more_triangles(self):
        z_list = [
            complex(u, v)**2
            for u in range(4, 7)
            for v in range(1, u)
        ]
        triangles = self.get_triangles(z_list)
        triangle = triangles[0]

        self.play(FadeOut(triangle))
        self.wait(2)
        for new_triangle in triangles[1:]:
            self.play(Transform(triangle, new_triangle))
            self.wait(2)

    ###

    def get_color_grid(self):
        width = (FRAME_X_RADIUS+abs(self.plane_center[0]))/self.initial_unit_size
        height = (FRAME_Y_RADIUS+abs(self.plane_center[1]))/self.initial_unit_size
        color_grid = ComplexPlane(
            x_radius = width,
            y_radius = int(height),
            secondary_line_ratio = 0,
            stroke_width = 2,
        )
        # CHANGE: typo in the original (color_grids is undefined, NameError also in Cairo)
        color_grid.set_color_by_gradient(
            *[GREEN, RED, MAROON_B, TEAL]*2
        )
        color_grid.remove(color_grid.axes[0])
        for line in color_grid.family_members_with_points():
            center = line.get_center()
            if center[0] <= 0 and abs(center[1]) < 0.01:
                line_copy = line.copy()
                line.scale(0.499, about_point = line.get_start())
                line_copy.scale(0.499, about_point = line_copy.get_end())
                color_grid.add(line_copy)
        color_grid.scale(self.initial_unit_size)
        color_grid.shift(self.plane_center)
        color_grid.prepare_for_nonlinear_transform()
        return color_grid

    def get_triangles(self, z_list):
        triangles = VGroup()
        for z in z_list:
            point = self.background_plane.number_to_point(z)
            line = Line(self.plane_center, point)
            triangle = Polygon(
                ORIGIN, RIGHT, RIGHT+UP,
                stroke_color = BLUE,
                stroke_width = 2,
                fill_color = BLUE,
                fill_opacity = 0.5,
            )
            triangle.replace(line, stretch = True)
            a = int(z.real)
            b = int(z.imag)
            c = int(abs(z))
            a_label, b_label, c_label = labels = [
                OldTex(str(num))
                for num in (a, b, c)
            ]
            for label in b_label, c_label:
                label.add_background_rectangle()
            a_label.next_to(triangle.get_bottom(), UP, SMALL_BUFF)
            b_label.next_to(triangle, RIGHT, SMALL_BUFF)
            c_label.next_to(line.get_center(), UP+LEFT, SMALL_BUFF)
            triangle.add(*labels)
            triangle.tip = point
            triangles.add(triangle)
        return triangles

    def homotopy(self, x, y, z, t):
        z_complex = self.background_plane.point_to_number(np.array([x, y, z]))
        result = z_complex**(1+t)
        return self.background_plane.number_to_point(result)


class PointsWeMiss(VisualizeZSquared):
    CONFIG = {
        "final_unit_size" : 0.4,
        "plane_center" : 2*LEFT + 2*DOWN,
        "dot_x_range" : list(range(-5, 6)),
        "dot_y_range" : list(range(-4, 4)),
    }
    def construct(self):
        self.add_plane()
        self.add_transformed_color_grid()
        self.add_dots()
        self.show_missing_point()
        self.show_second_missing_point()
        self.mention_one_half_rule()

    def add_transformed_color_grid(self):
        color_grid = self.get_color_grid()
        func = lambda p : self.homotopy(p[0], p[1], p[1], 1)
        color_grid.apply_function(func)
        color_grid.set_stroke(width = 4)
        self.add(color_grid, self.coordinate_labels)
        self.color_grid = color_grid

    def add_dots(self):
        z_list = [
            complex(x, y)**2
            for x in self.dot_x_range
            for y in self.dot_y_range
        ]
        dots = VGroup(*[
            Dot(
                self.background_plane.number_to_point(z),
                color = self.dot_color,
                radius = self.big_dot_radius,
            )
            for z in z_list
        ])
        dots.sort(get_norm)
        self.add(dots)
        self.dots = dots

    def show_missing_point(self):
        z_list = [complex(6, 8), complex(9, 12), complex(3, 4)]
        points = list(map(
            self.background_plane.number_to_point,
            z_list 
        ))
        dots = VGroup(*list(map(Dot, points)))
        for dot in dots[:2]:
            dot.set_stroke(RED, 4)
            dot.set_fill(opacity = 0)
        labels = VGroup(*[
            OldTex(complex_string_with_i(z))
            for z in z_list
        ])
        labels.set_color(RED)
        labels[2].set_color(GREEN)
        rhss = VGroup()
        for label, dot in zip(labels, dots):
            label.add_background_rectangle()
            label.next_to(dot, UP+RIGHT, SMALL_BUFF)
            if label is labels[-1]:
                rhs = OldTex("= (2+i)^2")
            else:
                rhs = OldTex("\\ne (u+vi)^2")
            rhs.add_background_rectangle()
            rhs.next_to(label, RIGHT)
            rhss.add(rhs)
        triangles = self.get_triangles(z_list)

        self.play(FocusOn(dots[0]))
        self.play(ShowCreation(dots[0]))
        self.play(Write(labels[0]))
        self.wait()
        self.play(FadeIn(triangles[0]))
        self.wait(2)
        self.play(Write(rhss[0]))
        self.wait(2)
        groups = triangles, dots, labels, rhss
        for i in 1, 2:
            self.play(*[
                Transform(group[0], group[i])
                for group in groups
            ])
            self.wait(3)
        self.play(*[
            FadeOut(group[0])
            for group in groups
        ])

    def show_second_missing_point(self):
        z_list = [complex(4, 3), complex(8, 6)]
        points = list(map(
            self.background_plane.number_to_point,
            z_list 
        ))
        dots = VGroup(*list(map(Dot, points)))
        dots[0].set_stroke(RED, 4)
        dots[0].set_fill(opacity = 0)
        labels = VGroup(*[
            OldTex(complex_string_with_i(z))
            for z in z_list
        ])
        labels[0].set_color(RED)
        labels[1].set_color(GREEN)
        rhss = VGroup()
        for label, dot in zip(labels, dots):
            label.add_background_rectangle()
            label.next_to(dot, UP+RIGHT, SMALL_BUFF)
            if label is labels[-1]:
                rhs = OldTex("= (3+i)^2")
            else:
                rhs = OldTex("\\ne (u+vi)^2")
            rhs.add_background_rectangle()
            rhs.next_to(label, RIGHT)
            rhss.add(rhs)
        triangles = self.get_triangles(z_list)
        groups = [dots, labels, rhss, triangles]
        for group in groups:
            group[0].save_state()

        self.play(ShowCreation(dots[0]))
        self.play(Write(VGroup(labels[0], rhss[0])))
        self.play(FadeIn(triangles[0]))
        self.wait(3)
        self.play(*[Transform(*group) for group in groups])
        self.wait(3)
        self.play(*[group[0].restore for group in groups])
        self.wait(2)

    def mention_one_half_rule(self):
        morty = Mortimer()
        morty.flip()
        morty.to_corner(DOWN+LEFT)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, 
            "Never need to scale \\\\ by less than $\\frac{1}{2}$"
        ))
        self.play(Blink(morty))
        self.wait(2)


class SupposeMissingPoint(PointsWeMiss):
    def construct(self):
        self.add_plane()
        self.background_plane.set_stroke(width = 1)
        self.draw_missing_triple()
        self.project_onto_unit_circle()

    def draw_missing_triple(self):
        point = self.background_plane.coords_to_point(12, 5)
        origin = self.plane_center
        line = Line(origin, point, color = WHITE)
        dot = Dot(point, color = YELLOW)
        triangle = Polygon(ORIGIN, RIGHT, RIGHT+UP)
        triangle.set_stroke(BLUE, 2)
        triangle.set_fill(BLUE, 0.5)
        triangle.replace(line, stretch = True)
        a = OldTex("a")
        a.next_to(triangle.get_bottom(), UP, SMALL_BUFF)
        b = OldTex("b")
        b.add_background_rectangle()
        b.next_to(triangle, RIGHT, SMALL_BUFF)
        c = OldTex("c")
        c.add_background_rectangle()
        c.next_to(line.get_center(), UP+LEFT, SMALL_BUFF)
        triangle.add(a, b, c)
        words = OldTexText(
            "If we missed \\\\ a triple \\dots"
        )
        words.add_background_rectangle()
        words.next_to(dot, UP+RIGHT)
        words.shift_onto_screen()

        self.add(triangle, line, dot)
        self.play(Write(words))
        self.wait()

        self.words = words
        self.triangle = triangle
        self.line = line
        self.dot = dot


    def project_onto_unit_circle(self):
        dot, line = self.dot, self.line
        template_line = Line(*[
            self.background_plane.number_to_point(n)
            for n in (-1, 1)
        ])
        circle = Circle(color = GREEN)
        circle.replace(template_line, dim_to_match = 0)
        z = self.background_plane.point_to_number(dot.get_center())
        z_norm = abs(z)
        unit_z = z/z_norm
        new_point = self.background_plane.number_to_point(unit_z)
        dot.generate_target()
        dot.target.move_to(new_point)
        line.generate_target()
        line.target.scale(1./z_norm, about_point = self.plane_center)

        rational_point_word = OldTex("(a/c) + (b/c)i")
        rational_point_word.next_to(
            self.background_plane.coords_to_point(0, 6), RIGHT
        )
        rational_point_word.add_background_rectangle()
        arrow = Arrow(
            rational_point_word.get_bottom(),
            dot.target,
            buff = SMALL_BUFF
        )

        self.play(ShowCreation(circle))
        self.add(dot.copy().fade())
        self.add(line.copy().set_stroke(GREY, 1))
        self.play(*list(map(MoveToTarget, [dot, line])))
        self.wait()
        self.play(
            Write(rational_point_word),
            ShowCreation(arrow)
        )
        self.wait(2)
