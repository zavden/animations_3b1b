# ==============================================================================
# Scene:      CirclePuzzle
# Source:     videos/_2025/colliding_blocks_v2/blocks.py (lines 1585-2192)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CirclePuzzle.py CirclePuzzle -w -m --fps 15
#
# Notes:
#   Not interactive: the 'while True' in get_lines is a geometric loop that ends with break. No changes.
# ==============================================================================

from manim_imports_ext import *

class CirclePuzzle(InteractiveScene):
    def construct(self):
        # Add axes
        x_axis, y_axis = axes = VGroup(Line(1.5 * LEFT, 1.5 * RIGHT), Line(UP, DOWN))
        axes.set_stroke(WHITE, 2, 0.33)
        axes.set_height(7)
        kw = dict(
            t2c={
                f"v_1": RED,
                f"v_2": RED,
                f"m_1": BLUE,
                f"m_2": BLUE,
            },
            font_size=24
        )
        axis_labels = VGroup(
            Tex(R"x = \sqrt{m_1} \cdot v_1", **kw).next_to(x_axis.get_right(), DOWN),
            Tex(R"y = \sqrt{m_2} \cdot v_2", **kw).next_to(y_axis.get_top(), RIGHT),
        )

        self.add(axes, axis_labels)

        # Add circle
        circle = Circle(radius=3)
        circle.set_stroke(YELLOW, 2)

        self.play(ShowCreation(circle))
        self.wait()

        # Set up lines
        slope_tracker = ValueTracker(-4)
        get_slope = slope_tracker.get_value
        lines = self.get_lines(circle, get_slope())

        state_point = Group(
            TrueDot(radius=0.05).make_3d(),
            GlowDot(radius=0.2),
        )
        state_point.set_color(RED)
        state_point.move_to(circle.get_left())

        self.play(FadeIn(state_point, shift=2 * DR, scale=0.25))
        self.wait()

        # Note the slope
        slope_label = Tex(R"\text{Slope} = -4.0", font_size=36)
        slope_label.next_to(lines[0].get_center(), RIGHT)
        slope_dec = slope_label.make_number_changeable("-4.0")
        count_label = Tex(R"\# \text{Lines} = 1", font_size=36)
        count = count_label.make_number_changeable("1")
        count_label.to_corner(UL)
        right_shift = (slope_dec.get_width() - count.get_width()) * RIGHT

        self.play(
            ShowCreation(lines[0]),
            state_point.animate.move_to(lines[0].get_end()),
            FadeIn(slope_label),
        )
        self.wait()
        self.play(
            slope_label.animate.next_to(count_label, DOWN, aligned_edge=RIGHT).shift(right_shift),
            VFadeIn(count_label),
            ChangeDecimalToValue(count, 2),
            ShowCreation(lines[1]),
            state_point.animate.move_to(lines[1].get_end()),
        )
        self.wait()

        # Show remaining lines
        for line in lines[2:]:
            self.play(
                ShowCreation(line),
                state_point.animate.move_to(line.get_end()),
                ChangeDecimalToValue(count, count.get_value() + 1)
            )
        self.wait()
        self.add(lines)

        # Show the end zone
        endzone = self.get_end_zone(-1.0 / get_slope())
        self.play(FadeIn(endzone))
        self.wait()

        # Ask the question
        count_rect = SurroundingRectangle(count_label)
        count_rect.set_stroke(PINK, 3)

        self.play(
            LaggedStart(
                (line.animate.set_stroke(PINK, 5).set_anim_args(rate_func=there_and_back)
                for line in lines),
                lag_ratio=0.5,
                run_time=6
            ),
            ShowCreation(count_rect)
        )

        # Vary the slope
        self.add(lines)
        lines.f_always.set_submobjects(lambda: self.get_lines(circle, get_slope()))
        count.f_always.set_value(lambda: len(lines))
        slope_dec.f_always.set_value(get_slope)
        endzone.f_always.become(lambda: self.get_end_zone(-1.0 / get_slope()))
        updated_pieces = [lines, count, slope_dec, endzone]

        slope_rect = SurroundingRectangle(slope_label)
        slope_rect.add_updater(lambda m: m.set_width(
            slope_label.get_width() + 2 * SMALL_BUFF,
            stretch=True,
            about_edge=LEFT
        ))

        self.play(
            ReplacementTransform(count_rect, slope_rect, suspend_mobject_updating=True),
            FadeOut(state_point),
        )
        self.play(
            slope_tracker.animate.set_value(-10),
            rate_func=there_and_back,
            run_time=10
        )
        for piece in updated_pieces:
            piece.suspend_updating()

        # Show slope equation
        rhs = Tex(R"= -\sqrt{m_1 / m_2}", **kw)
        rhs.scale(1.5)
        rhs.next_to(slope_label, RIGHT)

        mass_equations = VGroup(
            Tex(R"m_1 = 16", **kw),
            Tex(R"m_2 = 1", **kw),
        )
        mass_equations.scale(1.5)
        mass_equations.arrange(DOWN, aligned_edge=LEFT)
        mass_equations.next_to(slope_label, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            Write(rhs),
            FadeOut(slope_rect),
        )
        self.wait()
        self.play(
            TransformFromCopy(rhs["m_1"][0], mass_equations[0]["m_1"][0]),
            TransformFromCopy(rhs["m_2"][0], mass_equations[1]["m_2"][0]),
            FadeIn(mass_equations[0][2:]),
            FadeIn(mass_equations[1][2:]),
        )
        self.wait()
        self.add(mass_equations)

        # Increase slope
        mass_tracker = ValueTracker(16)
        get_mass_ratio = mass_tracker.get_value
        m1_dec = mass_equations[0].make_number_changeable("16")
        m1_dec.add_updater(lambda m: m.set_value(get_mass_ratio()))

        for piece in updated_pieces:
            piece.resume_updating()

        slope_tracker.add_updater(lambda m: m.set_value(-math.sqrt(int(get_mass_ratio()))))

        self.add(slope_tracker)
        self.play(
            mass_tracker.animate.set_value(100),
            rate_func=lambda t: there_and_back_with_pause(t, 0.1),
            run_time=12
        )

        for piece in updated_pieces:
            piece.suspend_updating()

        # Clear labels
        self.play(FadeOut(mass_equations), FadeOut(rhs))

        # Show arcs
        points = np.array([line.get_start() for line in lines] + [lines[-1].get_end()])
        dots = Group(state_point.copy().move_to(point) for point in points)
        arcs = self.get_arcs(points, slope=get_slope())
        for arc in arcs:
            arc.save_state()
            arc.scale(1.25, about_point=ORIGIN)
            arc.set_stroke(width=10, opacity=0)

        state_point.move_to(lines[0].get_start())
        self.add(dots[0])
        for line, dot in zip(lines, dots[1:]):
            self.play(state_point.animate.move_to(dot), run_time=0.5)
            self.add(dot)
        self.add(dots)
        self.play(FadeOut(state_point))

        self.play(LaggedStartMap(Restore, arcs, lag_ratio=0.25, run_time=3))
        self.wait()

        # Stack the arcs
        theta = math.atan(-1.0 / get_slope())
        stacked_arcs = VGroup(
            arc.copy().rotate(PI - angle_of_vector(arc.pfp(0.5)))
            for arc in arcs
        )
        stacked_arcs.arrange(RIGHT, buff=0.1)
        stacked_arcs.to_corner(DL)

        self.remove(circle)
        self.play(
            arcs.animate.set_stroke(opacity=0.25),
            TransformFromCopy(arcs, stacked_arcs, lag_ratio=0.35, run_time=4),
        )
        self.wait()
        self.play(
            Transform(
                stacked_arcs,
                arcs.copy().set_stroke(opacity=1),
                remover=True,
                lag_ratio=0.1,
            ),
            arcs.animate.set_stroke(opacity=1),
            run_time=3,
        )
        self.wait()

        # Show just two lines
        self.play(
            lines[:3].animate.set_stroke(opacity=0.15),
            lines[5:].animate.set_stroke(opacity=0.15),
            arcs[:4].animate.set_stroke(opacity=0.15),
            arcs[5:].animate.set_stroke(opacity=0.15),
            FadeOut(dots),
        )
        self.wait()

        # Mark the 2*theta arc
        lil_arc = Arc(-90 * DEG, theta, radius=1.5, arc_center=points[4])
        theta_label = Tex(R"\theta")
        theta_label.next_to(lil_arc.pfp(0.5), DOWN, SMALL_BUFF)
        new_lines = VGroup(
            Line(points[3], ORIGIN),
            Line(ORIGIN, points[5]),
        )
        new_lines.set_stroke(WHITE, 2)

        lil_two_arc = Arc(-PI + 4 * theta, 2 * theta, radius=1.0, arc_center=ORIGIN)
        two_theta_label = Tex(R"2\theta")
        two_theta_label.next_to(lil_two_arc.pfp(0.9), DL, SMALL_BUFF)

        self.play(
            ShowCreation(lil_arc),
            Write(theta_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(lines[3:5], new_lines),
            TransformFromCopy(lil_arc, lil_two_arc),
            TransformFromCopy(theta_label, two_theta_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(lil_two_arc, arcs[4]),
            two_theta_label.animate.next_to(arcs[4].pfp(0.5), DOWN, SMALL_BUFF),
            new_lines.animate.set_stroke(WHITE, 1),
        )
        self.wait()

        # Show the other lower arcs
        theta_group = VGroup(lil_arc, theta_label)
        for n in range(6, len(lines), 2):
            self.play(
                lines[n - 3:n - 1].animate.set_stroke(opacity=0.15),
                lines[n - 1:n + 1].animate.set_stroke(opacity=1),
                theta_group.animate.shift(points[n] - points[n - 2]),
                Rotate(new_lines, 2 * theta, about_point=ORIGIN),
                two_theta_label.animate.next_to(arcs[n].pfp(0.5), arcs[n].pfp(0.5), SMALL_BUFF),
                arcs[n - 2].animate.set_stroke(opacity=0.25),
                arcs[n].animate.set_stroke(opacity=1)
            )
            self.wait()

        # Show the upper arcs as well
        self.play(
            theta_group.animate.rotate(PI, about_point=points[10]).shift(points[1] - points[10]).scale(0.75, about_point=points[1]),
            Rotate(new_lines, -12 * theta, about_point=ORIGIN),
            two_theta_label.animate.next_to(arcs[1].pfp(0.5), arcs[1].pfp(0.5), buff=0.05),
            lines[9:11].animate.set_stroke(opacity=0.15),
            lines[0:2].animate.set_stroke(opacity=1),
            arcs[10].animate.set_stroke(opacity=0.15),
            arcs[1].animate.set_stroke(opacity=1),
            FadeOut(axis_labels),
            run_time=1,
        )
        self.wait()

        for n in range(3, len(lines), 2):
            self.play(
                lines[n - 3:n - 1].animate.set_stroke(opacity=0.15),
                lines[n - 1:n + 1].animate.set_stroke(opacity=1),
                theta_group.animate.shift(points[n] - points[n - 2]),
                Rotate(new_lines, -2 * theta, about_point=ORIGIN),
                two_theta_label.animate.next_to(arcs[n].pfp(0.5), arcs[n].pfp(0.5), SMALL_BUFF),
                arcs[n - 2].animate.set_stroke(opacity=0.25),
                arcs[n].animate.set_stroke(opacity=1)
            )
            self.wait()
        state_point.move_to(lines[0].get_start())
        self.play(
            FadeOut(two_theta_label),
            FadeOut(new_lines),
            FadeOut(theta_group),
            arcs[-1].animate.set_stroke(opacity=0.15),
            lines[-2:].animate.set_stroke(opacity=0.15),
            FadeIn(state_point),
        )

        # Show the process of dropping arcs while bouncing along diagram
        two_theta_labels = VGroup()
        past_state_points = Group()
        self.add(past_state_points)
        for line, arc in zip(lines, arcs):
            ghost_line = line.copy()
            ghost_arc = arc.copy()
            line.set_stroke(opacity=1)
            arc.set_stroke(opacity=1)

            two_theta_label = Tex(R"2\theta", font_size=36)
            two_theta_label.next_to(arc.pfp(0.5), arc.pfp(0.5), buff=0.05)
            two_theta_labels.add(two_theta_label)

            arc.save_state()
            arc.scale(1.25, about_point=ORIGIN)
            arc.set_stroke(width=12, opacity=0)

            past_state_points.add(state_point.copy())
            self.play(
                Animation(ghost_line, remover=True),
                Animation(ghost_arc, remover=True),
                ShowCreation(line),
                state_point.animate.move_to(line.get_end()),
                Restore(arc),
                FadeIn(two_theta_label, arc.saved_state.pfp(0.5) - arc.pfp(0.5)),
            )
        self.wait()

        # Emphasize endzone line
        max_x = 8
        endzone_line = Line(ORIGIN, max_x * RIGHT + max_x * -1.0 / get_slope() * UP)
        full_screen_rect = FullScreenFadeRectangle()
        full_screen_rect.set_fill(BLACK, 0.8)
        bold_lines = lines[0::2].copy()

        self.add(full_screen_rect, bold_lines)
        self.play(
            FadeIn(full_screen_rect),
            ShowCreation(endzone_line),
        )
        self.wait()
        self.play(
            FadeOut(full_screen_rect),
            FadeOut(bold_lines),
            FadeOut(endzone_line),
        )

        # Show end zone condition
        wedge = arcs[-1].copy()
        wedge.add_line_to(ORIGIN)
        wedge.add_line_to(arcs[-1].get_start())
        wedge.set_fill(PINK, 0.5)
        wedge.set_stroke(width=0)
        wedge.add(arcs[-1].copy().set_stroke(PINK))

        self.play(FadeIn(wedge))
        for angle in [-2 * theta, 10 * DEG, -10 * DEG, 5 * DEG, -5 * DEG]:
            self.play(Rotate(wedge, angle, about_point=ORIGIN))
            self.wait()

        self.play(FadeOut(wedge))

        # Bring back the mass ratio labels
        slope_label_rect = SurroundingRectangle(slope_label)
        slope_label_rect.set_stroke(YELLOW, 2)
        self.play(
            FadeIn(circle),
            FadeOut(two_theta_labels, lag_ratio=0.1),
            FadeOut(arcs, lag_ratio=0.1),
            FadeOut(past_state_points, lag_ratio=0.1),
            FadeOut(state_point),
        )
        self.play(ShowCreation(slope_label_rect))

        self.play(
            FadeIn(rhs),
            FadeIn(mass_equations),
        )
        self.wait()
        self.play(
            slope_label_rect.animate.surround(mass_equations).stretch(1.2, 0, about_edge=LEFT),
        )

        # Scale back up to 100
        self.add(lines)
        for piece in updated_pieces:
            piece.resume_updating()
        self.play(
            mass_tracker.animate.set_value(100),
            rhs.animate.shift(0.1 * RIGHT),
            run_time=5,
        )
        for piece in updated_pieces:
            piece.suspend_updating()

        # Make room
        frame = self.frame
        shift_value = 2.25 * LEFT
        line_index = 13

        movers = VGroup(count_label, slope_label, rhs, mass_equations)

        self.play(
            FadeOut(slope_label_rect, shift=shift_value),
            lines[:line_index + 1].animate.set_stroke(opacity=0.1),
            lines[line_index + 2:].animate.set_stroke(opacity=0.1),
            frame.animate.shift(shift_value),
            movers.animate.shift(shift_value),
        )

        # Show the slope
        dy_line = lines[line_index].copy().rotate(PI)
        dy_line.set_stroke(PINK, 3, 1)
        dx_line = Line(
            dy_line.get_end(),
            find_intersection(
                dy_line.get_end(),
                RIGHT,
                lines[line_index + 1].get_start(),
                lines[line_index + 1].get_vector(),
            )
        )
        dx_line.set_stroke(RED, 5)

        dy_label = Tex(R"\Delta y", font_size=36).match_color(dy_line)
        dx_label = Tex(R"\Delta x", font_size=36).match_color(dx_line)
        dy_label.next_to(dy_line, LEFT, SMALL_BUFF).shift(0.25 * DOWN)
        dx_label.next_to(dx_line, UP, SMALL_BUFF)

        slope_tex_kw = dict(
            t2c={
                R"\Delta y": PINK,
                R"\Delta x": RED,
            },
            font_size=36
        )
        new_slope_eq = Tex(R"\text{Slope} = {\Delta y \over \Delta x}", **slope_tex_kw)
        new_slope_eq.next_to(slope_label, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            FadeIn(new_slope_eq, DOWN),
            mass_equations.animate.to_edge(DOWN),
        )
        self.wait()
        self.play(
            ShowCreation(dy_line),
            TransformFromCopy(new_slope_eq[R"\Delta y"][0], dy_label)
        )
        self.wait()
        self.play(
            ShowCreation(dx_line),
            TransformFromCopy(new_slope_eq[R"\Delta x"][0], dx_label)
        )
        self.wait()

        # Show the angle
        theta = math.atan(-1 / get_slope())
        point = dy_line.get_start()
        arc = Arc(-90 * DEG, theta, radius=2.25, arc_center=point)
        theta_label = Tex(R"\theta", font_size=36)
        theta_label.next_to(arc, DOWN, SMALL_BUFF)

        tan_eq = Tex(R"\tan(\theta) = {\Delta x \over -\Delta y}", **slope_tex_kw)
        tan_eq.next_to(new_slope_eq, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            ShowCreation(arc),
            Write(theta_label),
        )
        self.play(
            TransformFromCopy(theta_label, tan_eq[R"\theta"]),
            Write(tan_eq[R"\tan("]),
            Write(tan_eq[R") = "]),
        )
        self.wait()
        self.play(
            TransformFromCopy(dx_label, tan_eq[R"\Delta x"][0]),
        )
        self.play(
            TransformFromCopy(dy_label, tan_eq[R"\Delta y"][0]),
            Write(tan_eq[R"\over"]),
            Write(tan_eq[R"-"]),
        )
        self.wait()

        # Relate tangent to slope
        kw["font_size"] = 36
        new_rhs = Tex(R"= \sqrt{m_2 / m_1}", **kw)
        new_rhs.next_to(tan_eq, RIGHT, SMALL_BUFF)

        new_rhs_brace = Brace(new_rhs[1:], UP, SMALL_BUFF)
        ratio_example = new_rhs_brace.get_text("0.1", buff=SMALL_BUFF, font_size=36)

        arctan_eq = Tex(R"\theta = \arctan\left(\sqrt{m_2 / m_1}\right)", **kw)
        arctan_eq.next_to(tan_eq, DOWN, buff=0.5, aligned_edge=LEFT)

        example_arctan = Tex(R"\theta = \arctan(0.1)", font_size=36)
        example_arctan.next_to(arctan_eq, DOWN, buff=0.5, aligned_edge=LEFT)

        example_arctan_rect = SurroundingRectangle(example_arctan)

        self.play(
            LaggedStart(
                TransformFromCopy(new_slope_eq[R"\Delta y"], tan_eq[R"\Delta y"], path_arc=-90 * DEG),
                TransformFromCopy(new_slope_eq[R"\Delta x"], tan_eq[R"\Delta x"], path_arc=-90 * DEG),
                run_time=2
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                rhs.copy(),
                new_rhs,
                path_arc=-90 * DEG,
                run_time=2,
                lag_ratio=0.01,
                matched_keys=["m_1", "m_2", R"\sqrt"],
            )
        )
        self.wait()
        self.play(
            GrowFromCenter(new_rhs_brace),
            TransformFromCopy(mass_equations.copy().clear_updaters(), ratio_example),
        )
        self.wait()

        self.play(LaggedStart(
            TransformFromCopy(tan_eq[R"\tan"], arctan_eq[R"\arctan"]),
            TransformFromCopy(tan_eq[R"("], arctan_eq[R"\left("]),
            TransformFromCopy(tan_eq[R")"], arctan_eq[R"\right)"]),
            TransformFromCopy(tan_eq[R"\theta"], arctan_eq[R"\theta"]),
            TransformFromCopy(tan_eq[R"="], arctan_eq[R"="]),
            TransformFromCopy(new_rhs[R"\sqrt{m_2 / m_1}"], arctan_eq[R"\sqrt{m_2 / m_1}"]),
            lag_ratio=0.1,
            run_time=2
        ))
        self.wait()
        self.play(FadeIn(example_arctan, DOWN))
        self.play(ShowCreation(example_arctan_rect))
        self.wait()

    def get_lines(self, circle, slope, stroke_color=WHITE, stroke_width=2):
        theta = math.atan(-1.0 / slope)
        radius = 0.5 * circle.get_width()

        top_point = circle.get_left()
        low_point = rotate_vector(top_point, 2 * theta)

        result = VGroup()

        while True:
            if math.atan2(top_point[1], top_point[0]) < theta:
                # In the end zone
                break
            result.add(Line(top_point, low_point))
            top_point = rotate_vector(top_point, -2 * theta)
            if top_point[1] < 0:
                break
            result.add(Line(low_point, top_point))
            low_point = rotate_vector(low_point, 2 * theta)

        result.set_stroke(stroke_color, stroke_width)
        return result

    def get_end_zone(self, slope, max_x=8, color=GREEN, opacity=0.25):
        zone = Polygon(
            max_x * RIGHT + slope * max_x * UP,
            ORIGIN, 
            max_x * RIGHT
        )
        zone.set_stroke(color, 0)
        zone.set_fill(color, opacity)
        label = Text("End Zone", font_size=36)
        label.set_color(color)
        label.next_to(zone.get_bottom(), UP, SMALL_BUFF)
        label.to_edge(RIGHT, buff=0.5)

        return VGroup(zone, label)

    def get_arcs(self, points, slope):
        # Test
        theta = math.atan(-1.0 / slope)
        arcs = VGroup()
        for i in range(-1, len(points) - 2):
            arc = Line(
                points[max(i, 0)],
                points[i + 2],
                path_arc=-2 * theta * (-1)**(i % 2)
            )
            color = [BLUE, BLUE, RED, RED][i % 4]
            arc.set_stroke(color, width=4)
            arcs.add(arc)

        return arcs
