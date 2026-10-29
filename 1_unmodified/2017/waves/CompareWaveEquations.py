# ==============================================================================
# Scene:      CompareWaveEquations
# Source:     videos/_2017/waves.py (lines 3848-4018)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareWaveEquations.py CompareWaveEquations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class CompareWaveEquations(TeacherStudentsScene):
    def construct(self):
        self.add_equation()
        self.show_complex_plane()
        self.show_interpretations()

    def add_equation(self):
        equation = OldTex(
            "|\\!\\psi\\rangle",
            "=", "\\alpha", "|\\!\\rightarrow\\rangle",
            "+", "\\beta", "|\\!\\uparrow\\rangle",
        )
        equation.set_color_by_tex_to_color_map({
            "psi" : BLUE,
            "rightarrow" : RED,
            "uparrow" : GREEN,
        })
        equation.next_to(ORIGIN, LEFT)
        equation.to_edge(UP)

        psi_rect = SurroundingRectangle(equation.get_part_by_tex("psi"))
        psi_rect.set_color(WHITE)
        state_words = OldTexText("Polarization \\\\ state")
        state_words.set_color(BLUE)
        state_words.scale(0.8)
        state_words.next_to(psi_rect, DOWN)

        equation.save_state()
        equation.scale(0.01)
        equation.fade(1)
        equation.move_to(self.teacher.get_left())
        equation.shift(SMALL_BUFF*UP)

        self.play(
            equation.restore,
            self.teacher.change, "raise_right_hand",
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = psi_rect,
            added_anims = [
                ShowCreation(psi_rect),
                Write(state_words, run_time = 1)
            ],
            run_time = 1
        )
        self.play(FadeOut(psi_rect))

        self.equation = equation
        self.state_words = state_words

    def show_complex_plane(self):
        new_alpha, new_beta = terms = [
            self.equation.get_part_by_tex(tex).copy()
            for tex in ("alpha", "beta")
        ]
        for term in terms:
            term.save_state()
            term.generate_target()
            term.target.scale(0.7)

        plane = ComplexPlane(
            x_radius = 1.5,
            y_radius = 1.5,
        )
        plane.add_coordinates()
        plane.scale(1.3)
        plane.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        plane.to_edge(UP)

        alpha_dot, beta_dot = [
            Dot(
                plane.coords_to_point(x, 0.5), 
                radius = 0.05,
                color = color
            )
            for x, color in [(-0.5, RED), (0.5, GREEN)]
        ]
        new_alpha.target.next_to(alpha_dot, UP+LEFT, 0.5*SMALL_BUFF)
        new_alpha.target.set_color(RED)
        new_beta.target.next_to(beta_dot, UP+RIGHT, 0.5*SMALL_BUFF)
        new_beta.target.set_color(GREEN)

        rhs = OldTex(
            "=", "A_y", "e", "^{i(", 
            "2\\pi", "f", "t", "+", "\\phi_y", ")}"
        )
        rhs.scale(0.7)
        rhs.next_to(new_beta.target, RIGHT, SMALL_BUFF)
        rhs.shift(0.5*SMALL_BUFF*UP)
        rhs.set_color_by_tex_to_color_map({
            "A_y" : GREEN,
            "phi" : MAROON_B,
        })
        A_copy = rhs.get_part_by_tex("A_y").copy()
        phi_copy = rhs.get_part_by_tex("phi_y").copy()
        A_line = Line(
            plane.coords_to_point(0, 0),
            plane.coords_to_point(0.5, 0.5),
            color = GREEN,
            stroke_width = 2,
        )

        arc = Arc(angle = np.pi/4, radius = 0.5)
        arc.shift(plane.get_center())

        self.play(
            Write(plane, run_time = 2),
            MoveToTarget(new_alpha),
            MoveToTarget(new_beta),
            DrawBorderThenFill(alpha_dot, run_time = 1),
            DrawBorderThenFill(beta_dot, run_time = 1),
        )
        self.play(
            Write(rhs),
            ShowCreation(A_line),
            ShowCreation(arc)
        )
        self.play(
            phi_copy.next_to, arc, RIGHT, SMALL_BUFF,
            phi_copy.shift, 0.5*SMALL_BUFF*UP
        )
        self.play(
            A_copy.next_to, A_line.get_center(), 
                UP, SMALL_BUFF,
            A_copy.shift, 0.5*SMALL_BUFF*(UP+LEFT),
        )
        self.wait()

    def show_interpretations(self):
        c_words = OldTex(
            "\\text{Classically: }", "&|\\beta|^2",
            "\\rightarrow",
            "\\text{Component of} \\\\",
            "&\\text{energy in }", "|\\!\\uparrow\\rangle", 
            "\\text{ direction}",
        )
        qm_words = OldTex(
            "\\text{Quantum: }", "&|\\beta|^2",
            "\\rightarrow",
            "\\text{Probability that}", "\\text{ \\emph{all}} \\\\",
            "&\\text{energy is measured in }", "|\\!\\uparrow\\rangle", 
            "\\text{ direction}",
        )
        for words in c_words, qm_words:
            words.set_color_by_tex_to_color_map({
                "Classically" : YELLOW,
                "Quantum" : BLUE,
                "{all}" : BLUE,
                "beta" : GREEN,
                "uparrow" : GREEN,
            })
            words.scale(0.7)
        c_words.to_edge(LEFT)
        c_words.shift(2*UP)
        qm_words.next_to(c_words, DOWN, MED_LARGE_BUFF, LEFT)

        self.play(
            FadeOut(self.state_words),
            Write(c_words),
            self.teacher.change, "happy"
        )
        self.play_student_changes(
            *["happy"]*3, look_at = c_words
        )
        self.play(Write(qm_words))
        self.play_student_changes(
            "erm", "confused", "pondering",
            look_at = qm_words
        )
        self.wait()
