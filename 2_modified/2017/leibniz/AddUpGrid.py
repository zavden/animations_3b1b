# ==============================================================================
# Scene:      AddUpGrid
# Source:     videos/_2017/leibniz.py (lines 4230-4615)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AddUpGrid.py AddUpGrid -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in GL a scene created by hand needs setup(); cairo_nested_scene does it
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


class CountLatticePointsInBigCircle(LatticePointScene):
    CONFIG = {
        "y_radius" : 2*11,
        "max_lattice_point_radius" : 10,
        "dot_radius" : 0.05
    }
    def construct(self):
        self.resize_plane()
        self.introduce_points()
        self.show_rings()
        self.ignore_center_dot()

    def resize_plane(self):
        self.plane.set_stroke(width = 2)
        self.plane.scale(2)
        self.lattice_points.scale(2)
        for point in self.lattice_points:
            point.scale(0.5)

    def introduce_points(self):
        circle = self.get_circle(radius = self.max_lattice_point_radius)
        radius = Line(ORIGIN, circle.get_right())
        radius.set_color(RED)
        R = OldTex("R").next_to(radius, UP)
        R_rect = BackgroundRectangle(R)
        R_group = VGroup(R_rect, R)
        pi_R_squared = OldTex("\\pi", "R", "^2")
        pi_R_squared.next_to(ORIGIN, UP)
        pi_R_squared.to_edge(RIGHT)
        pi_R_squared_rect = BackgroundRectangle(pi_R_squared)
        pi_R_squared_group = VGroup(pi_R_squared_rect, pi_R_squared)

        self.play(*list(map(FadeIn, [circle, radius, R_group])))
        self.add_foreground_mobject(R_group)
        self.draw_lattice_points()
        self.wait()
        self.play(
            FadeOut(R_rect),
            FadeIn(pi_R_squared_rect),
            ReplacementTransform(R, pi_R_squared.get_part_by_tex("R")),
            Write(VGroup(*[
                part for part in pi_R_squared
                if part is not pi_R_squared.get_part_by_tex("R")
            ]))
        )
        self.remove(R_group)
        self.add_foreground_mobject(pi_R_squared_group)
        self.wait()

        self.circle = circle
        self.radius = radius

    def show_rings(self):
        N_range = list(range(self.max_lattice_point_radius**2))
        rings = VGroup(*[
            self.get_circle(radius = np.sqrt(N))
            for N in N_range
        ])
        rings.set_color_by_gradient(TEAL, GREEN)
        rings.set_stroke(width = 2)
        dot_groups = VGroup(*[
            self.get_lattice_points_on_r_squared_circle(N)
            for N in N_range
        ])
        radicals = self.get_radicals()

        self.play(
            LaggedStartMap(FadeIn, rings),
            Animation(self.lattice_points),
            LaggedStartMap(FadeIn, radicals),
            run_time = 3
        )
        self.add_foreground_mobject(radicals)
        self.play(
            LaggedStartMap(
                ApplyMethod,
                dot_groups,
                lambda m : (m.set_stroke, PINK, 5),
                rate_func = there_and_back,
                run_time = 4,
                lag_ratio = 0.1,
            ),
        )
        self.wait()

        self.rings = rings

    def ignore_center_dot(self):
        center_dot = self.lattice_points[0]
        circle = Circle(color = RED)
        circle.replace(center_dot)
        circle.scale(2)
        arrow = Arrow(ORIGIN, UP+RIGHT, color = RED)
        arrow.next_to(circle, DOWN+LEFT, SMALL_BUFF)
        new_max = 2*self.max_lattice_point_radius
        new_dots = VGroup(*[
            Dot(
                self.plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            for x in range(-new_max, new_max+1)
            for y in range(-new_max, new_max+1)
            if (x**2 + y**2) > self.max_lattice_point_radius**2
            if (x**2 + y**2) < new_max**2
        ])
        new_dots.sort(get_norm)

        self.play(*list(map(ShowCreation, [circle, arrow])))
        self.play(*list(map(FadeOut, [circle, arrow])))
        self.play(FadeOut(center_dot))
        self.lattice_points.remove(center_dot)
        self.wait()
        self.play(*[
            ApplyMethod(m.scale, 0.5)
            for m in [
                self.plane,
                self.circle,
                self.radius,
                self.rings,
                self.lattice_points
            ]
        ])
        new_dots.scale(0.5)
        self.play(FadeOut(self.rings))
        self.play(
            ApplyMethod(
                VGroup(self.circle, self.radius).scale, 2,
                rate_func=linear,
            ),
            LaggedStartMap(
                DrawBorderThenFill,
                new_dots,
                stroke_width = 4,
                stroke_color = PINK,
                lag_ratio = 0.2,
            ),
            run_time = 4,
        )
        self.wait(2)

    #####

    @staticmethod
    def get_radicals():
        radicals = VGroup(*[
            OldTex("\\sqrt{%d}"%N)
            for N in range(1, 13)
        ])
        radicals.add(
            OldTex("\\vdots"),
            OldTex("\\sqrt{R^2}")
        )
        radicals.arrange(DOWN, buff = MED_SMALL_BUFF)
        radicals.set_height(FRAME_HEIGHT - MED_LARGE_BUFF)
        radicals.to_edge(DOWN, buff = MED_SMALL_BUFF)
        radicals.to_edge(LEFT)
        for radical in radicals:
            radical.add_background_rectangle()
        return radicals


class AddUpGrid(Scene):
    def construct(self):
        self.add_radicals()
        self.add_row_lines()
        self.add_chi_sums()
        self.put_four_in_corner()
        self.talk_through_rows()
        self.organize_into_columns()
        self.add_count_words()
        self.collapse_columns()
        self.factor_out_R()
        self.show_chi_sum_values()
        self.compare_to_pi_R_squared()
        self.celebrate()

    def add_radicals(self):
        self.radicals = CountLatticePointsInBigCircle.get_radicals()
        self.add(self.radicals)

    def add_row_lines(self):
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS - MED_LARGE_BUFF)
        h_line.set_stroke(WHITE, 1)
        row_lines = VGroup(*[
            h_line.copy().next_to(
                radical, DOWN,
                buff = SMALL_BUFF,
                aligned_edge = LEFT
            )
            for radical in self.radicals
        ])
        row_lines[-2].shift(
            row_lines[-1].get_left()[0]*RIGHT -\
            row_lines[-2].get_left()[0]*RIGHT
        )

        self.play(LaggedStartMap(ShowCreation, row_lines))
        self.wait()

        self.row_lines = row_lines

    def add_chi_sums(self):
        chi_sums = VGroup()
        chi_mobs = VGroup()
        plusses = VGroup()
        fours = VGroup()
        parens = VGroup()
        arrows = VGroup()
        for N, radical in zip(list(range(1, 13)), self.radicals):
            arrow, four, lp, rp = list(map(Tex, [
                "\\Rightarrow", "4", "\\big(", "\\big)"
            ]))
            fours.add(four)
            parens.add(lp, rp)
            arrows.add(arrow)
            chi_sum = VGroup(arrow, four, lp)
            for d in range(1, N+1):
                if N%d != 0:
                    continue
                chi_mob = OldTex("\\chi(", str(d), ")")
                chi_mob[1].set_color(YELLOW)
                chi_mob.d = d
                chi_mobs.add(chi_mob)
                chi_sum.add(chi_mob)
                if d != N:
                    plus = OldTex("+")
                    plus.chi_mob = chi_mob
                    plusses.add(plus)
                    chi_sum.add(plus)
            chi_sum.add(rp)
            chi_sum.arrange(RIGHT, buff = SMALL_BUFF)
            chi_sum.scale(0.7)
            chi_sum.next_to(radical, RIGHT)
            chi_sums.add(chi_sum)
            radical.chi_sum = chi_sum

        self.play(LaggedStartMap(
            Write, chi_sums, 
            run_time = 5,
            rate_func = lambda t : t,
        ))
        self.wait()

        digest_locals(self, [
            "chi_sums", "chi_mobs", "plusses", 
            "fours", "parens", "arrows",
        ])

    def put_four_in_corner(self):
        corner_four = OldTex("4")
        corner_four.to_corner(DOWN+RIGHT, buff = MED_SMALL_BUFF)
        rect = SurroundingRectangle(corner_four, color = BLUE)
        corner_four.rect = rect

        self.play(
            ReplacementTransform(
                self.fours, VGroup(corner_four),
                run_time = 2,
            ),
            FadeOut(self.parens)
        )
        self.play(ShowCreation(rect))

        self.corner_four = corner_four

    def talk_through_rows(self):
        rect = Rectangle(
            stroke_width = 0,
            fill_color = BLUE_C,
            fill_opacity = 0.3,
        )
        rect.stretch_to_fit_width(
            VGroup(self.radicals, self.chi_mobs).get_width()
        )
        rect.stretch_to_fit_height(self.radicals[0].get_height())

        composite_rects, prime_rects = [
            VGroup(*[
                rect.copy().move_to(self.radicals[N-1], LEFT)
                for N in numbers
            ])
            for numbers in ([6, 12], [2, 3, 5, 7, 11])
        ]
        prime_rects.set_color(GREEN)

        randy = Randolph().flip()
        randy.next_to(self.chi_mobs, RIGHT)

        self.play(FadeIn(randy))
        self.play(randy.change_mode, "pleading")
        self.play(
            FadeIn(composite_rects),
            randy.look_at, composite_rects.get_bottom()
        )
        self.wait(2)
        self.play(
            FadeOut(composite_rects),
            FadeIn(prime_rects),
            randy.look_at, prime_rects.get_top(),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(*list(map(FadeOut, [prime_rects, randy])))

    def organize_into_columns(self):
        left_x = self.arrows.get_right()[0] + SMALL_BUFF
        spacing = self.chi_mobs[-1].get_width() + SMALL_BUFF
        for chi_mob in self.chi_mobs:
            y = chi_mob.get_left()[1]
            x = left_x + (chi_mob.d - 1)*spacing
            chi_mob.generate_target()
            chi_mob.target.move_to(x*RIGHT + y*UP, LEFT)
        for plus in self.plusses:
            plus.generate_target()
            plus.target.scale(0.5)
            plus.target.next_to(
                plus.chi_mob.target, RIGHT, SMALL_BUFF
            )

        self.play(*it.chain(
            list(map(MoveToTarget, self.chi_mobs)),
            list(map(MoveToTarget, self.plusses)),
        ), run_time = 2)
        self.wait()

    def add_count_words(self):
        rect = Rectangle(
            stroke_color = WHITE,
            stroke_width = 2,
            fill_color = average_color(BLUE_E, BLACK),
            fill_opacity = 1,
            height = 1.15,
            width = FRAME_WIDTH - 2*MED_SMALL_BUFF,
        )
        rect.move_to(3*LEFT, LEFT)
        rect.to_edge(UP, buff = SMALL_BUFF)
        words = OldTexText("Total")
        words.scale(0.8)
        words.next_to(rect.get_left(), RIGHT, SMALL_BUFF)
        approx = OldTex("\\approx")
        approx.scale(0.7)
        approx.next_to(words, RIGHT, SMALL_BUFF)
        words.add(approx)

        self.play(*list(map(FadeIn, [rect, words])))
        self.wait()

        self.count_rect = rect
        self.count_words = words

    def collapse_columns(self):
        chi_mob_columns = [VGroup() for i in range(12)]
        for chi_mob in self.chi_mobs:
            chi_mob_columns[chi_mob.d - 1].add(chi_mob)

        full_sum = VGroup()
        for d in range(1, 7):
            R_args = ["{R^2"]
            if d != 1:
                R_args.append("\\over %d}"%d)
            term = VGroup(
                OldTex(*R_args),
                OldTex("\\chi(", str(d), ")"),
                OldTex("+")
            )
            term.arrange(RIGHT, SMALL_BUFF)
            term[1][1].set_color(YELLOW)
            full_sum.add(term)
        full_sum.arrange(RIGHT, SMALL_BUFF)
        full_sum.scale(0.7)
        full_sum.next_to(self.count_words, RIGHT, SMALL_BUFF)

        for column, term in zip(chi_mob_columns, full_sum):
            rect = SurroundingRectangle(column)
            rect.stretch_to_fit_height(FRAME_HEIGHT)
            rect.move_to(column, UP)
            rect.set_stroke(width = 0)
            rect.set_fill(YELLOW, 0.3)

            self.play(FadeIn(rect))
            self.wait()
            self.play(
                ReplacementTransform(
                    column.copy(),
                    VGroup(term[1]),
                    run_time = 2
                ),
                Write(term[0]),
                Write(term[2]),
            )
            self.wait()
            if term is full_sum[2]:
                vect = sum([
                    self.count_rect.get_left()[0],
                    FRAME_X_RADIUS,
                    -MED_SMALL_BUFF,
                ])*LEFT
                self.play(*[
                    ApplyMethod(m.shift, vect)
                    for m in [
                        self.count_rect,
                        self.count_words,
                    ]+list(full_sum[:3])
                ])
                VGroup(*full_sum[3:]).shift(vect)
            self.play(FadeOut(rect))

        self.full_sum = full_sum

    def factor_out_R(self):
        self.corner_four.generate_target()
        R_squared = OldTex("R^2")
        dots = OldTex("\\cdots")
        lp, rp = list(map(Tex, ["\\big(", "\\big)"]))
        new_sum = VGroup(
            self.corner_four.target, R_squared, lp
        )

        R_fracs, chi_terms, plusses = full_sum_parts = [
            VGroup(*[term[i] for term in self.full_sum])
            for i in range(3)
        ]
        targets = []
        for part in full_sum_parts:
            part.generate_target()
            targets.append(part.target)
        for R_frac, chi_term, plus in zip(*targets):
            chi_term.scale(0.9)
            chi_term.move_to(R_frac[0], DOWN)
            if R_frac is R_fracs.target[0]:
                new_sum.add(chi_term)
            else:
                new_sum.add(VGroup(chi_term, R_frac[1]))
            new_sum.add(plus)
        new_sum.add(dots)
        new_sum.add(rp)
        new_sum.arrange(RIGHT, buff = SMALL_BUFF)
        new_sum.next_to(self.count_words, RIGHT, SMALL_BUFF)
        R_squared.shift(0.5*SMALL_BUFF*UP)
        R_movers = VGroup()
        for R_frac in R_fracs.target:
            if R_frac is R_fracs.target[0]:
                mover = R_frac
            else:
                mover = R_frac[0]
            Transform(mover, R_squared).update(1)
            R_movers.add(mover)

        self.play(*it.chain(
            list(map(Write, [lp, rp, dots])), 
            list(map(MoveToTarget, full_sum_parts)),
        ), run_time = 2)
        self.remove(R_movers)
        self.add(R_squared)
        self.wait()
        self.play(
            MoveToTarget(self.corner_four, run_time = 2),
            FadeOut(self.corner_four.rect)
        )
        self.wait(2)
        self.remove(self.full_sum, self.corner_four)
        self.add(new_sum)

        self.new_sum = new_sum

    def show_chi_sum_values(self):
        alt_rhs = OldTex(
            "\\approx", "4", "R^2", 
            "\\left(1 - \\frac{1}{3} + \\frac{1}{5}" + \
            "-\\frac{1}{7} + \\frac{1}{9} - \\frac{1}{11}" + \
            "+ \\cdots \\right)",
        )
        alt_rhs.scale(0.9)
        alt_rhs.next_to(
            self.count_words[-1], DOWN,
            buff = LARGE_BUFF,
            aligned_edge = LEFT
        )

        self.play(
            *list(map(FadeOut, [
                self.chi_mobs, self.plusses, self.arrows,
                self.radicals, self.row_lines
            ])) + [
            FadeOut(self.count_rect),
            Animation(self.new_sum),
            Animation(self.count_words),
            ]
        )
        self.play(Write(alt_rhs))
        self.wait(2)

        self.alt_rhs = alt_rhs

    def compare_to_pi_R_squared(self):
        approx, pi, R_squared = area_rhs = OldTex(
            "\\approx", "\\pi", "R^2"
        )
        area_rhs.next_to(self.alt_rhs, RIGHT)

        brace = Brace(
            VGroup(self.alt_rhs, area_rhs), DOWN
        )
        brace.add(brace.get_text(
            "Arbitrarily good as $R \\to \\infty$"
        ))

        pi_sum = OldTex(
            "4", self.alt_rhs[-1].get_tex(),
            "=", "\\pi"
        )
        pi_sum.scale(0.9)
        pi = pi_sum.get_part_by_tex("pi")
        pi.scale(2, about_point = pi.get_left())
        pi.set_color(YELLOW)
        pi_sum.shift(
            self.alt_rhs[-1].get_bottom(),
            MED_SMALL_BUFF*DOWN,
            -pi_sum[1].get_top()
        )

        self.play(Write(area_rhs))
        self.wait()
        self.play(FadeIn(brace))
        self.wait(2)
        self.play(FadeOut(brace))
        self.play(*[
            ReplacementTransform(m.copy(), pi_sum_part)
            for pi_sum_part, m in zip(pi_sum, [
                self.alt_rhs.get_part_by_tex("4"),
                self.alt_rhs[-1],
                area_rhs[0],
                area_rhs[1],
            ])
        ])

    def celebrate(self):
        # CHANGE: in GL a scene created by hand needs setup(); cairo_nested_scene does it
        creatures = cairo_nested_scene(TeacherStudentsScene).get_pi_creatures()
        self.play(FadeIn(creatures))
        self.play(*[
            ApplyMethod(pi.change, "hooray", self.alt_rhs)
            for pi in creatures
        ])
        self.wait()
        for i in 0, 2, 3:
            self.play(Blink(creatures[i]))
            self.wait()
