# ==============================================================================
# Scene:      BasicVectorFieldIdea
# Source:     videos/_2021/matrix_exp.py (lines 5200-5434)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BasicVectorFieldIdea.py BasicVectorFieldIdea -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VectorField/StreamLines are imported from legacy_arrow_vector_field (arrow API with func(x, y) and step_multiple, from before Sept 2024).
# ==============================================================================

from manim_imports_ext import *
# CHANGE: VectorField/StreamLines with manimgl's arrow API from before Sept 2024 (see _lib/legacy_arrow_vector_field.py)
from legacy_arrow_vector_field import VectorField, StreamLines

def mat_exp(matrix, N=100):
    curr = np.identity(len(matrix))
    curr_sum = curr
    for n in range(1, N):
        curr = np.dot(curr, matrix) / n
        curr_sum += curr
    return curr_sum


class BasicVectorFieldIdea(Scene):
    matrix = [[-1.5, -1], [3, 0.5]]

    def construct(self):
        # Equation
        v_tex = "\\vec{\\textbf{v} }(t)"
        equation = OldTex(
            "{d \\over dt}", v_tex, "=", "M", v_tex,
            tex_to_color_map={
                "M": GREY_A,
                v_tex: YELLOW,
            }
        )
        equation.set_height(1.5)
        equation.to_corner(UL, buff=0.25)

        background_rect = SurroundingRectangle(equation, buff=SMALL_BUFF)
        background_rect.set_fill(BLACK, opacity=0.9).set_stroke(WHITE, 2)

        # Plane and field
        matrix = np.array(self.matrix)

        def func(x, y):
            return 0.15 * np.dot(matrix.T, [x, y])

        plane = NumberPlane()
        vector_field = VectorField(
            func, plane,
            magnitude_range=(0, 2),
            vector_config={"thickness": 0.025}
        )
        dots = VGroup(*(
            Dot(v.get_start(), radius=0.02, fill_color=YELLOW)
            for v in vector_field
        ))

        # Velocity and position
        vel_rect = SurroundingRectangle(equation[:2], stroke_color=RED)
        pos_rect = SurroundingRectangle(equation[4], stroke_color=YELLOW)
        pos_rect.match_height(vel_rect, stretch=True)
        pos_rect.match_y(vel_rect)

        vel_words = Text("Velocity", color=RED)
        vel_words.next_to(vel_rect, DOWN)
        vel_words.shift_onto_screen(buff=0.2)
        pos_words = Text("Position", color=YELLOW)
        pos_words.next_to(pos_rect, DOWN)

        for word in vel_words, pos_words:
            word.add_background_rectangle()

        self.add(plane, background_rect, equation)

        self.play(
            ShowCreation(vel_rect),
            FadeIn(vel_words, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            ShowCreation(pos_rect),
            FadeIn(pos_words, 0.5 * DOWN),
        )
        self.wait()
        term_labels = VGroup(vel_rect, vel_words, pos_rect, pos_words)

        foreground = [background_rect, equation, term_labels]
        self.add(dots, *foreground)
        self.play(LaggedStartMap(GrowFromCenter, dots))
        self.add(dots, vector_field, *foreground)
        self.play(LaggedStartMap(GrowArrow, vector_field, lag_ratio=0.01))
        self.wait()
        self.play(
            FadeOut(dots),
            FadeOut(term_labels),
            vector_field.animate.set_opacity(0.25)
        )

        # Show Mv being attached to v
        index = 326
        lil_vect = vector_field[index]
        coords = plane.p2c(lil_vect.get_start())

        dot = Dot(color=YELLOW, radius=0.05)
        dot.move_to(plane.c2p(*coords))
        dot_label = OldTex("\\vec{\\textbf{v}}", color=YELLOW)
        dot_label.next_to(dot, UR, SMALL_BUFF)

        vector = Arrow(plane.get_origin(), dot.get_center(), buff=0)
        vector.set_fill(YELLOW, opacity=1)
        vector.set_stroke(BLACK, 0.5)

        Mv = Arrow(plane.get_origin(), plane.c2p(*3 * func(*coords)), buff=0)
        Mv.set_fill(RED, 1)
        Mv_label = OldTex("M", "\\vec{\\textbf{v}}")
        Mv_label[0].set_color(GREY_B)
        Mv_label.next_to(Mv.get_end(), DOWN)
        attached_Mv = lil_vect.copy().set_opacity(1)

        self.play(
            GrowFromPoint(dot, equation[-1].get_center()),
            FadeTransform(equation[-1][0].copy(), dot_label),
        )
        self.wait()
        self.play(
            FadeIn(vector),
            ReplacementTransform(vector.copy().set_opacity(0), Mv, path_arc=-45 * DEGREES),
            FadeTransform(equation[3:5].copy(), Mv_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(Mv, attached_Mv)
        )
        self.remove(attached_Mv)
        lil_vect.set_opacity(1)
        self.wait()

        for x in range(100):
            index += 1
            lil_vect = vector_field[index]
            coords = plane.p2c(lil_vect.get_start())
            vector.put_start_and_end_on(plane.get_origin(), plane.c2p(*coords))
            Mv.put_start_and_end_on(plane.get_origin(), plane.c2p(*3 * func(*coords)))
            Mv_label.next_to(Mv.get_end(), DOWN)
            dot.move_to(vector.get_end())
            dot_label.next_to(dot, UR, SMALL_BUFF)
            lil_vect.set_opacity(1)

            if x < 20:
                self.wait(0.25)
            else:
                self.wait(0.1)

        self.play(
            LaggedStartMap(FadeOut, VGroup(Mv_label, dot_label, Mv, vector, dot)),
            vector_field.animate.set_opacity(1)
        )
        self.wait()

        # Show example initial condition evolving
        def get_flow_lines(step_multiple, arc_len):
            return StreamLines(
                func, plane,
                step_multiple=step_multiple,
                magnitude_range=(0, 2),
                color_by_magnitude=False,
                stroke_color=GREY_A,
                stroke_width=2,
                stroke_opacity=1,
                arc_len=arc_len,
            )

        dot = Dot()
        vect = Vector()
        vect.set_color(RED)

        def update_vect(vect):
            coords = plane.p2c(dot.get_center())
            end = plane.c2p(*func(*coords))
            vect.put_start_and_end_on(plane.get_origin(), end)
            vect.shift(dot.get_center() - plane.get_origin())

        vect.add_updater(update_vect)

        flow_line = get_flow_lines(4, 20)[10]
        flow_line.insert_n_curves(100)
        flow_line.set_stroke(width=3)
        dot.move_to(flow_line.get_start())

        self.add(flow_line, vect, dot)
        self.play(
            MoveAlongPath(dot, flow_line, run_time=10, rate_func=linear),
            ShowCreation(flow_line, run_time=10, rate_func=linear),
            VFadeIn(dot),
            VFadeIn(vect),
        )
        self.play(LaggedStartMap(FadeOut, VGroup(flow_line, dot, vect)))
        self.wait()

        # Show exponential solution
        solution = OldTex(
            v_tex, "=", "e^{M t}", "\\vec{\\textbf{v} }(0)"
        )

        solution[0].set_color(YELLOW)
        solution[2][1].set_color(GREY_B)
        solution.match_width(equation)
        solution.next_to(equation, DOWN, MED_LARGE_BUFF)

        new_br = SurroundingRectangle(VGroup(equation, solution), buff=MED_SMALL_BUFF)
        new_br.match_style(background_rect)

        self.play(
            Transform(background_rect, new_br),
            FadeIn(solution, 0.5 * DOWN)
        )
        self.wait()
        foreground = VGroup(background_rect, equation, solution)
        self.play(FadeOut(foreground))

        # Show flow of all initial conditions
        initial_points = np.array([
            plane.c2p(x, y)
            for x in np.arange(-16, 16, 0.5)
            for y in np.arange(-6, 6, 0.5)
        ])
        dots = DotCloud(initial_points)
        dots.set_radius(0.06)
        dots.set_color(WHITE)
        initial_points = np.array(dots.get_points())

        self.add(dots)
        self.play(vector_field.animate.set_opacity(0.75))

        time_tracker = ValueTracker()

        def update_dots(dots):
            time = time_tracker.get_value()
            transformation = np.identity(3)
            transformation[:2, :2] = mat_exp(0.15 * matrix * time)
            dots.set_points(np.dot(initial_points, transformation))

        streaks = Group()

        def update_streaks(streaks):
            dc = dots.copy()
            dc.clear_updaters()
            dc.set_opacity(0.25)
            dc.set_radius(0.01)
            streaks.add(dc)

        dots.add_updater(update_dots)
        streaks.add_updater(update_streaks)

        self.add(plane, vector_field, streaks, dots)
        self.play(time_tracker.animate.set_value(3), run_time=6, rate_func=linear)
