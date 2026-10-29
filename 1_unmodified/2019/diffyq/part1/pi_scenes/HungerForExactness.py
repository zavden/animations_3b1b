# ==============================================================================
# Scene:      HungerForExactness
# Source:     videos/_2019/diffyq/part1/pi_scenes.py (lines 315-506)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl HungerForExactness.py HungerForExactness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/pi_scenes.py -----

class HungerForExactness(TeacherStudentsScene):
    def construct(self):
        students = self.students
        you = students[2]
        teacher = self.teacher

        ode = get_ode()
        ode.to_corner(UL)
        left_part = ode[:5]
        friction_part = ode[5:11]
        self.add(ode)

        proposed_solution = OldTex(
            "\\theta_0\\cos((\\sqrt{g/L})t)e^{-\\mu t}"
        )
        proposed_solution.next_to(
            you.get_corner(UL), UP, buff=0.7
        )
        proposed_solution_rect = SurroundingRectangle(
            proposed_solution, buff=MED_SMALL_BUFF,
        )
        proposed_solution_rect.set_color(BLUE)
        proposed_solution_rect.round_corners()

        solution_p1 = OldTex(
            """
            \\theta(t) = 2\\text{am}\\left(
                \\frac{\\sqrt{2g + Lc_1} (t + c_2)}{2\\sqrt{L}},
                \\frac{4g}{2g + Lc_1}
            \\right)
            """,
        )
        solution_p1.to_corner(UL)
        solution_p2 = OldTex(
            "c_1, c_2 = \\text{Constants depending on initial conditions}"
        )
        solution_p2.set_color(GREY_B)
        solution_p2.scale(0.75)
        solution_p3 = OldTex(
            """
            \\text{am}(u, k) =
            \\int_0^u \\text{dn}(v, k)\\,dv
            """
        )
        solution_p3.name = OldTexText(
            "(Jacobi amplitude function)"
        )
        solution_p4 = OldTex(
            """
            \\text{dn}(u, k) =
            \\sqrt{1 - k^2 \\sin^2(\\phi)}
            """
        )
        solution_p4.name = OldTexText(
            "(Jacobi elliptic function)"
        )
        solution_p5 = OldTexText("Where $\\phi$ satisfies")
        solution_p6 = OldTex(
            """
            u = \\int_0^\\phi \\frac{dt}{\\sqrt{1 - k^2 \\sin^2(t)}}
            """
        )

        solution = VGroup(
            solution_p1,
            solution_p2,
            solution_p3,
            solution_p4,
            solution_p5,
            solution_p6,
        )
        solution.arrange(DOWN)
        solution.scale(0.7)
        solution.to_corner(UL, buff=MED_SMALL_BUFF)
        solution.set_stroke(width=0, background=True)

        solution.remove(solution_p2)
        solution_p1.add(solution_p2)
        solution.remove(solution_p5)
        solution_p6.add(solution_p5)

        for part in [solution_p3, solution_p4]:
            part.name.scale(0.7 * 0.7)
            part.name.set_color(GREY_B)
            part.name.next_to(part, RIGHT)
            part.add(part.name)

        self.student_says(
            "Right, but like,\\\\"
            "what \\emph{is} $\\theta(t)$?",
            target_mode="sassy",
            added_anims=[teacher.change, "guilty"],
        )
        self.wait()
        self.play(
            FadeInFromDown(proposed_solution),
            RemovePiCreatureBubble(
                you,
                target_mode="raise_left_hand",
                look_at=proposed_solution,
            ),
            teacher.change, "pondering",
            students[0].change, "pondering",
            students[1].change, "hesitant",
        )
        self.play(ShowCreation(proposed_solution_rect))
        self.play(
            proposed_solution.shift, 3 * RIGHT,
            proposed_solution_rect.shift, 3 * RIGHT,
            you.change, "raise_right_hand", teacher.eyes,
        )
        self.wait(3)

        self.play(
            FadeOut(proposed_solution),
            FadeOut(proposed_solution_rect),
            ode.move_to, self.hold_up_spot, DOWN,
            ode.shift, LEFT,
            teacher.change, "raise_right_hand",
            self.change_students(*3 * ["pondering"])
        )
        self.wait()
        ode.save_state()
        self.play(
            left_part.move_to, friction_part, RIGHT,
            left_part.match_y, left_part,
            friction_part.to_corner, DR,
            friction_part.fade, 0.5,
        )
        self.wait()

        modes = ["erm", "sad", "sad", "horrified"]
        for part, mode in zip(solution, modes):
            self.play(
                FadeIn(part, UP),
                self.change_students(
                    *3 * [mode],
                    look_at=part,
                )
            )
            self.wait()
        self.wait(3)
        self.play_student_changes("tired", "sad", "concerned_musician")
        self.wait(4)
        self.look_at(solution)
        self.wait(5)
        self.play(
            FadeOut(solution, 2 * LEFT),
            Restore(ode),
            self.change_students(
                "sick", "angry", "tired",
            )
        )
        self.wait(3)

        mystery = OldTex(
            "\\theta(t) = ???",
            tex_to_color_map={"\\theta": BLUE},
        )
        mystery.scale(2)
        mystery.to_edge(UP)
        mystery.set_stroke(width=0, background=True)
        mystery_boundary = AnimatedBoundary(
            mystery, stroke_width=1
        )

        self.play(
            FadeInFromDown(mystery),
            self.teacher.change, "pondering"
        )
        self.add(mystery_boundary, mystery)
        self.play_all_student_changes("sad")
        self.look_at(mystery)
        self.wait(5)

        # Define
        self.student_says(
            "Let $\\text{P}(\\mu, g, L; t)$ be a\\\\"
            "function satisfying this ODE.",
            index=0,
            target_mode="speaking",
            added_anims=[
                FadeOut(mystery),
                FadeOut(mystery_boundary),
                ode.to_corner, UR
            ]
        )
        self.play_student_changes(
            "hooray", "sassy", "sassy",
            look_at=students[0].eyes.get_corner(UR),
        )
        self.wait(2)
