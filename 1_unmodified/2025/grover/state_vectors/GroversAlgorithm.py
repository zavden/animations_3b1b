# ==============================================================================
# Scene:      GroversAlgorithm
# Source:     videos/_2025/grover/state_vectors.py (lines 2266-2860)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl GroversAlgorithm.py GroversAlgorithm -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/qc_supplements.py -----

def get_key_icon(height=0.5):
    key_icon = SVGMobject("key").rotate(135 * DEG)
    key_icon.set_fill(YELLOW)
    key_icon.set_height(height)
    return key_icon



# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)


class GroversAlgorithm(InteractiveScene):
    def construct(self):
        # Set up plane
        x_range = y_range = (-1, 1 - 1e-6)
        plane = NumberPlane(x_range, y_range, faded_line_ratio=5)
        plane.set_height(6)
        plane.background_lines.set_stroke(BLUE, 1, 1)
        plane.faded_lines.set_stroke(BLUE, 1, 0.25)

        self.add(plane)

        # Add key and balance directions
        key_vect = Vector(plane.c2p(0, 1), thickness=5, fill_color=YELLOW)
        b_vect = key_vect.copy().rotate(- np.arccos(1 / math.sqrt(3)), about_point=ORIGIN)
        b_vect.set_fill(TEAL)

        key_label, b_label = labels = VGroup(
            KetGroup(Tex(char))
            for char in "kb"
        )
        labels.set_submobject_colors_by_gradient(YELLOW, TEAL)
        labels.set_backstroke(BLACK, 3)
        for label in labels:
            label[1].shift(0.02 * UR)
        key_label.next_to(key_vect.get_end(), UP, SMALL_BUFF)
        b_label.next_to(b_vect.get_end(), UR, SMALL_BUFF)
        key_icon = get_key_icon()
        key_icon.set_height(0.75 * key_label.get_height())
        key_icon.next_to(key_label, LEFT, SMALL_BUFF)

        self.add(key_vect, b_vect)
        self.add(key_label, b_label, key_icon)
        self.wait()

        # Highlight key
        self.play(GrowArrow(key_vect))
        self.play(FlashAround(key_label, time_width=1.5, run_time=2))

        # Label the x-direction
        x_vect = Vector(plane.c2p(1, 0), thickness=5)
        x_vect.set_fill(WHITE)
        x_label_example, x_label_general = x_labels = VGroup(
            Tex(R"\frac{1}{\sqrt{2}}\big(|0\rangle + |1\rangle \big)", font_size=36),
            Tex(R"\frac{1}{\sqrt{N - 1}} \sum_{n \ne k} |n \rangle", font_size=24),
        )
        for label in x_labels:
            label.next_to(x_vect.get_end(), RIGHT)

        x_label_general.shift(SMALL_BUFF * DL)

        self.play(
            TransformFromCopy(key_vect, x_vect, path_arc=-90 * DEG),
            FadeIn(x_label_general, time_span=(0.5, 1.5)),
        )
        self.wait()

        x_label_general.save_state()
        self.play(
            FadeIn(x_label_example, DOWN),
            x_label_general.animate.fade(0.5).shift(1.25 * DOWN),
        )
        self.wait()

        # Show component of b in the direction of key
        rhs = Tex(R"= \frac{1}{\sqrt{3}}\big(|0\rangle + |1\rangle + |2\rangle \big)", font_size=36)
        rhs.next_to(b_label, RIGHT)
        rhs.set_color(TEAL)

        b_vect_proj = Vector(plane.c2p(0, plane.p2c(b_vect.get_end())[1]), thickness=5)
        b_vect_proj.set_fill(TEAL_E, 1)
        dashed_line = DashedLine(b_vect.get_end(), b_vect_proj.get_end())

        self.play(FadeIn(rhs, lag_ratio=0.1))
        self.wait()
        self.play(
            TransformFromCopy(b_vect, b_vect_proj),
            ShowCreation(dashed_line),
        )
        self.wait()
        self.play(
            FlashAround(rhs[R"|2\rangle"], time_width=1.5, run_time=3),
            rhs[R"|2\rangle"].animate.set_color(YELLOW),
        )
        self.wait()

        # Set up N
        N_eq = Tex(R"N = 3")
        dim = N_eq.make_number_changeable("3", edge_to_fix=LEFT)
        N_eq.next_to(plane, UR, LARGE_BUFF).shift_onto_screen()

        self.play(
            LaggedStart(
                FadeOut(rhs),
                Restore(x_label_general),
                FadeOut(x_label_example, 0.5 * UP),
            ),
            Write(N_eq)
        )

        # Increase N
        N_tracker = ValueTracker(3)
        get_N = N_tracker.get_value

        def update_b_vects(vects):
            N = int(get_N())
            x = math.sqrt(1 - 1.0 / N)
            y = 1 / math.sqrt(N)
            vects[0].put_start_and_end_on(plane.c2p(0, 0), plane.c2p(x, y))
            vects[1].put_start_and_end_on(plane.c2p(0, 0), plane.c2p(0, y))

        self.play(
            N_tracker.animate.set_value(100).set_anim_args(rate_func=rush_into),
            UpdateFromFunc(dim, lambda m: m.set_value(int(get_N()))),
            UpdateFromFunc(VGroup(b_vect, b_vect_proj), update_b_vects),
            UpdateFromFunc(dashed_line, lambda m: m.become(DashedLine(b_vect.get_end(), b_vect_proj.get_end()))),
            UpdateFromFunc(b_label, lambda m: m.next_to(b_vect.get_end(), UR, SMALL_BUFF)),
            run_time=12
        )
        self.wait()

        # Reference the angle
        alpha = math.acos(1 / math.sqrt(N_tracker.get_value()))
        arc = Arc(90 * DEG, -alpha, radius=0.5)
        alpha_label = Tex(R"\alpha")
        alpha_label.next_to(arc.pfp(0.5), UR, SMALL_BUFF)
        lt_90 = Tex(R"< 90^\circ")
        lt_90.next_to(alpha_label, RIGHT).shift(0.05 * UL)

        self.play(
            FadeOut(b_vect_proj),
            FadeOut(dashed_line),
            ShowCreation(arc),
            FadeIn(alpha_label),
        )
        self.play(Write(lt_90))
        self.wait()
        self.play(FadeIn(VGroup(b_vect_proj, dashed_line), run_time=3, rate_func=there_and_back_with_pause, remover=True))
        self.wait()

        # Show the dot product
        frame = self.frame

        b_comp_tex = R"1 / \sqrt{N}"
        b_array = TexMatrix(np.array([
            *2 * [b_comp_tex],
            R"\vdots",
            *3 * [b_comp_tex],
            R"\vdots",
            *2 * [b_comp_tex],
        ]).reshape(-1, 1))
        k_array = TexMatrix(np.array([
            *2 * ["0"],
            R"\vdots",
            "0", "1", "0",
            R"\vdots",
            *2 * ["0"],
        ]).reshape(-1, 1))
        arrays = VGroup(k_array, b_array)

        for array in arrays:
            array.set_height(6)

        arrays.arrange(LEFT, buff=MED_LARGE_BUFF)
        arrays.next_to(plane, RIGHT, buff=2.5).to_edge(DOWN, buff=MED_LARGE_BUFF)
        dot = Tex(R"\cdot", font_size=72)
        dot.move_to(midpoint(b_array.get_right(), k_array.get_left()))

        k_array_label, b_array_label = array_labels = labels.copy()

        for label, arr in zip(array_labels, arrays):
            arr.set_fill(interpolate_color(label.get_fill_color(), WHITE, 0.2), 1)
            label.next_to(arr, UP, MED_LARGE_BUFF)

        self.play(
            GrowFromPoint(b_array, b_label.get_center()),
            TransformFromCopy(b_label, b_array_label),
            N_eq.animate.to_edge(UP, MED_SMALL_BUFF).set_x(2),
            frame.animate.set_x(4),
            FadeOut(x_label_general),
            FadeOut(x_vect),
            run_time=2
        )
        self.play(
            GrowFromPoint(k_array, key_label.get_center()),
            TransformFromCopy(key_label, k_array_label),
            Write(dot),
            run_time=2
        )
        self.wait()

        # Evaluate the dot product
        elem_rects = VGroup(
            SurroundingRectangle(VGroup(*elems), buff=0.05).set_width(2.5, stretch=True)
            for elems in zip(b_array.elements, k_array.elements)
        )
        for rect in elem_rects:
            rect.set_stroke(WHITE, 2)
            rect.align_to(elem_rects[0], RIGHT)

        equals = Tex(R"=").next_to(arrays, RIGHT)
        rhs = Tex(R"1 / \sqrt{N}")
        rhs.next_to(equals, RIGHT)

        self.play(Write(equals))
        self.play(
            LaggedStartMap(VFadeInThenOut, elem_rects, lag_ratio=0.2, run_time=5),
            FadeIn(rhs, time_span=(1.75, 2.25)),
        )
        self.wait()

        # Show cosine expression
        cos_expr = Tex(R"\cos(\alpha) = 1 / \sqrt{N}", font_size=36)
        cos_expr.next_to(alpha_label, UP, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(LaggedStart(
            FadeOut(lt_90),
            Write(cos_expr[R"\cos("]),
            Write(cos_expr[R") ="]),
            TransformFromCopy(alpha_label, cos_expr[R"\alpha"][0]),
            TransformFromCopy(rhs, cos_expr[R"1 / \sqrt{N}"][0]),
            lag_ratio=0.1,
        ))
        self.wait()

        # Show sine of smaller angle
        target_thickness = 3

        for vect in [b_vect, key_vect]:
            vect.target = Arrow(ORIGIN, vect.get_end(), thickness=target_thickness, buff=0)
            vect.target.match_style(vect)

        theta = 90 * DEG - alpha
        theta_arc = Arc(0, theta, radius=2.0)
        theta_label = Tex(R"\theta", font_size=24)
        theta_label.next_to(theta_arc, RIGHT, buff=0.1)
        alpha_label.set_backstroke(BLACK, 5)
        theta_label.set_backstroke(BLACK, 5)

        sin_expr = Tex(R"\sin(\theta) = 1 / \sqrt{N}", font_size=36)
        sin_expr.move_to(cos_expr).set_y(-0.5)

        theta_approx = Tex(R"\theta \approx 1 / \sqrt{N}", font_size=36)
        theta_approx.next_to(sin_expr, DOWN, aligned_edge=RIGHT)

        cos_group = VGroup(arc, alpha_label, cos_expr)

        self.play(
            MoveToTarget(b_vect),
            MoveToTarget(key_vect),
            LaggedStart(
                TransformFromCopy(arc, theta_arc),
                TransformFromCopy(alpha_label, theta_label),
                TransformFromCopy(cos_expr, sin_expr),
                lag_ratio=0.25
            ),
            cos_group.animate.fade(0.5)
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                sin_expr.copy(),
                theta_approx,
                matched_keys=[R"1 / \sqrt{N}"],
                key_map={"=": R"\approx"}
            )
        )
        self.wait()

        # Put it in the corner
        self.play(
            LaggedStartMap(FadeOut, VGroup(array_labels, arrays, dot, equals, rhs, cos_group, sin_expr), lag_ratio=0.25),
            frame.animate.set_x(-2),
            N_eq.animate.set_x(-2),
            theta_approx.animate.to_corner(UR, buff=MED_SMALL_BUFF).shift(2 * LEFT),
            run_time=2
        )
        self.wait()

        # Add vector components
        vector = b_vect.copy()

        initial_coords = 0.1 * np.ones(11)
        vect_coords = DecimalMatrix(initial_coords.reshape(-1, 1), num_decimal_places=3, decimal_config=dict(include_sign=True))
        vect_coords.set_height(6)
        vect_coords.next_to(frame.get_left(), RIGHT, MED_LARGE_BUFF)
        mid_index = len(initial_coords) // 2
        dot_indices = [mid_index - 2, mid_index + 2]
        arr_dots = VGroup()
        for index in dot_indices:
            element = vect_coords.elements[index]
            dots = Tex(R"\vdots")
            dots.move_to(element)
            element.become(dots)
            arr_dots.add(element)

        vect_coords.set_fill(GREY_B)

        def update_vect_coords(vect_coords):
            x, y = plane.p2c(vector.get_end())
            x /= math.sqrt(99)
            for n, elem in enumerate(vect_coords.elements):
                if n in dot_indices:
                    continue
                elif n == mid_index:
                    elem.set_value(y)
                else:
                    elem.set_value(x)

        vect_coords.add_updater(update_vect_coords)

        key_icon2 = get_key_icon(height=0.25)
        key_icon2.next_to(vect_coords, LEFT, SMALL_BUFF)

        self.add(vect_coords)
        self.add(key_icon2)

        # Add bars
        min_bar_width = 0.125
        bar_height = 0.25

        dec_elements = VGroup(
            elem for n, elem in enumerate(vect_coords.elements) if n not in dot_indices
        )
        bars = Rectangle(min_bar_width, bar_height).replicate(len(dec_elements))
        bars.set_fill(opacity=1)
        bars.set_submobject_colors_by_gradient(BLUE, GREEN)
        bars.set_stroke(WHITE, 0.5)

        for bar, elem in zip(bars, dec_elements):
            bar.next_to(vect_coords, RIGHT)
            bar.match_y(elem)
            bar.elem = elem

        def update_bars(bars):
            x, y = plane.p2c(vector.get_end())
            x /= math.sqrt(99)
            mid_index = len(bars) // 2
            for n, bar in enumerate(bars):
                if n == mid_index:
                    prob = 1 - 99 * (x**2)
                else:
                    prob = x**2
                width = min_bar_width * np.sqrt(prob / 0.01)
                bar.set_width(width, about_edge=LEFT, stretch=True)

        self.add(bars)

        # Show the flips
        circle = Circle(radius=0.5 * plane.get_width())
        circle.set_stroke(WHITE, 1)
        b_vect.set_fill(opacity=0.5)

        frame.set_field_of_view(20 * DEG)

        diag_line = DashedLine(-b_vect.get_end(), b_vect.get_end())
        h_line = DashedLine(plane.get_left(), plane.get_right())
        VGroup(h_line, diag_line).set_stroke(WHITE, 2)

        flip_line = h_line.copy()

        flipper = VGroup(circle, vector)

        vect_ghosts = VGroup()

        def right_filp(run_time=2):
            self.play(
                Rotate(flipper, PI, RIGHT, about_point=ORIGIN),
                vect_ghosts.animate.set_fill(opacity=0.25),
                run_time=run_time
            )

        def diag_flip(run_time=2, draw_time=0.5):
            self.play(ShowCreation(diag_line, run_time=draw_time))
            self.play(
                flipper.animate.flip(axis=diag_line.get_vector(), about_point=ORIGIN),
                vect_ghosts.animate.set_fill(opacity=0.25),
                UpdateFromFunc(bars, update_bars),
                run_time=run_time
            )
            self.play(FadeOut(diag_line, run_time=2 * draw_time))

        self.add(vect_ghosts, vector)
        self.play(FadeIn(circle))
        for n in range(4):
            vect_ghosts.add(vector.copy())
            right_filp()
            self.wait()
            vect_ghosts.add(vector.copy())
            diag_flip(draw_time=(0.5 if n < 2 else 1 / 30))
            self.wait()

        vect_ghosts.add(vect.copy()).set_fill(opacity=0.25)

        # Show vertical component
        if False:  # For an insertion
            # Show vert component
            self.add(diag_line)

            x, y = plane.p2c(vector.get_end())
            v_part = Arrow(plane.get_origin(), plane.c2p(0, y), thickness=4, buff=0, max_width_to_length_ratio=0.25)
            v_part.set_fill(GREEN)
            h_line = DashedLine(vector.get_end(), v_part.get_end())
            brace = Brace(v_part, LEFT, buff=0.05)

            self.play(
                FadeOut(diag_line),
                TransformFromCopy(vector, v_part),
                ShowCreation(h_line),
            )
            self.wait()
            self.play(GrowFromCenter(brace))
            self.wait()

        # Show steps of 2 * theta
        bars.add_updater(update_bars)

        arcs = VGroup(
            Arc(n * theta, 2 * theta, radius=circle.get_radius())
            for n in range(1, len(vect_ghosts), 2)
        )
        for arc, color in zip(arcs, it.cycle([BLUE, RED])):
            arc.set_stroke(color, 3)

        arc_labels = VGroup(
            Tex(R"2\theta", font_size=24).next_to(arc.pfp(0.5), normalize(arc.pfp(0.5)), SMALL_BUFF)
            for arc in arcs
        )

        self.play(
            Rotate(
                vector,
                -angle_between_vectors(vector.get_vector(), b_vect.get_vector()),
                about_point=ORIGIN
            ),
            FadeOut(b_label)
        )
        self.wait()
        right_filp()
        diag_flip(draw_time=0.25)
        self.wait()
        self.play(
            TransformFromCopy(vect_ghosts[0], vector, path_arc=theta),
            ShowCreation(arcs[0])
        )
        self.play(TransformFromCopy(theta_label, arc_labels[0]))
        self.wait()
        for arc, label in zip(arcs[1:], arc_labels[1:]):
            self.play(
                Rotate(vector, 2 * theta, about_point=ORIGIN),
                ShowCreation(arc),
                FadeIn(label, shift=0.5 * (arc.get_end() - arc.get_start()))
            )
            self.wait()

        # Show full angle
        quarter_arc = Arc(0, 90 * DEG)
        ninety_label = Tex(R"90^\circ")
        pi_halves_label = Tex(R"\pi / 2")
        for label in [ninety_label, pi_halves_label]:
            label.set_backstroke(BLACK, 5)
            label.next_to(quarter_arc.pfp(0.5), UR, buff=0.05)

        self.play(
            ShowCreation(quarter_arc),
            Write(ninety_label),
        )
        self.wait()
        self.play(FadeTransform(ninety_label, pi_halves_label))
        self.wait()

        # Calculate n steps
        lhs = Text("# Repetitions")
        lhs.next_to(plane, RIGHT, buff=1.0).set_y(2)
        rhs_terms = VGroup(
            Tex(R"\approx {\pi / 2 \over 2 \theta}"),
            Tex(R"= {\pi \over 4} \cdot {1 \over \theta}"),
            Tex(R"= {\pi \over 4} \sqrt{N}"),
        )
        rhs_terms.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        rhs_terms.shift(lhs.get_right() + 0.2 * RIGHT + 0.05 * UP - rhs_terms[0].get_left())

        self.play(
            frame.animate.set_x(3),
            FadeOut(vect_coords),
            FadeOut(bars),
            FadeOut(key_icon2),
            Write(lhs),
            Write(rhs_terms[0]),
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, rhs_terms[1:], shift=0.5 * DOWN, lag_ratio=0.5))
        self.wait()

        # Collapse
        self.play(LaggedStart(
            Rotate(
                vector,
                -angle_between_vectors(vector.get_vector(), b_vect.get_vector()),
                about_point=ORIGIN
            ),
            FadeOut(arcs),
            FadeOut(arc_labels),
            FadeOut(vect_ghosts),
            FadeOut(b_vect),
            FadeOut(theta_label),
            FadeOut(theta_arc),
            frame.animate.set_y(0.5),
            N_eq.animate.shift(0.5 * UP),
            theta_approx.animate.align_to(plane, RIGHT),
            VGroup(lhs, rhs_terms).animate.shift(1.5 *  UP)
        ))

        # Increment to 2^20
        new_theta = math.asin(2**(-10))
        dim.set_value(100)
        step_count = Tex(R"\frac{\pi}{4}\sqrt{2^{20}} = 804.248...")
        step_count.next_to(rhs_terms, DOWN, LARGE_BUFF)
        step_count.to_edge(RIGHT).shift(frame.get_x() * RIGHT)

        eq_two_twenty = Tex(R"=2^{20}")
        eq_two_twenty.next_to(N_eq["="], DOWN, aligned_edge=LEFT)

        self.play(
            ChangeDecimalToValue(dim, int(2**20)),
            Rotate(vector, new_theta - theta, about_point=ORIGIN),
            FadeIn(eq_two_twenty, time_span=(0, 1)),
            run_time=3
        )
        self.wait()
        self.play(
            TransformFromCopy(rhs_terms[-1][1:6], step_count[:5]),
            TransformFromCopy(eq_two_twenty[1:], step_count["2^{20}"][0]),
            run_time=2
        )
        self.play(Write(step_count["= 804.248..."][0]))
        self.wait()

        # Change vector
        step_tracker = ValueTracker(0)
        radius = 0.5 * plane.get_width()

        step_label = Tex(R"\#\text{Reps} = 0", font_size=36)
        step_label.next_to(plane.c2p(-0.6, 0), UP, SMALL_BUFF)
        step_count = step_label.make_number_changeable(0, edge_to_fix=UL)
        step_count.f_always.set_value(lambda: 0.5 * step_tracker.get_value())

        shadows = VectorizedPoint().replicate(300)

        def update_vector(vector):
            steps = int(step_tracker.get_value())
            if steps % 2 == 0:
                angle = new_theta * (steps + 1)
            else:
                angle = -new_theta * steps
            point = rotate_vector(radius * RIGHT, angle)
            vector.put_start_and_end_on(ORIGIN, point)
            shadows.remove(shadows[0])
            shadows.add(vector.copy())
            shadows.clear_updaters()
            for n, shadow in enumerate(shadows[::-1]):
                shadow.set_fill(opacity=0.75 / (n + 1))

        self.play(FadeIn(step_label))
        self.add(shadows)
        self.add(vect_coords, bars)
        self.play(
            step_tracker.animate.set_value(2 * 804),
            UpdateFromFunc(vector, update_vector),
            frame.animate.scale(1.4, about_edge=RIGHT).set_anim_args(time_span=(0, 8)),
            run_time=20,
            rate_func=linear,
        )
        self.play(FadeOut(shadows, lag_ratio=0.1, run_time=1))
        self.wait()

    def key_flip_insertion(self):
        # Test
        self.clear()
        key_ghost = key_vect.copy().set_fill(opacity=0.5)
        self.add(key_ghost)
        self.play(
            key_vect.animate.flip(axis=RIGHT, about_edge=DOWN),
            run_time=2
        )
        self.wait()

    def thumbnail_insertion(self):
        # Test
        plane.background_lines.set_stroke(BLUE, 8, 1)
        plane.faded_lines.set_stroke(BLUE, 5, 0.25)
        circle.set_stroke(WHITE, 3)
        self.remove(N_eq)
        self.remove(theta_label)
        self.remove(theta_arc)
        self.remove(theta_approx)
