# ==============================================================================
# Scene:      FactorOrdinaryNumber
# Source:     videos/_2017/leibniz.py (lines 1869-1939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FactorOrdinaryNumber.py FactorOrdinaryNumber -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FactorOrdinaryNumber(TeacherStudentsScene):
    def construct(self):
        equation = OldTex(
            "2{,}250", "=", "2 \\cdot 3^2 \\cdot 5^3"
        )
        equation.next_to(self.get_pi_creatures(), UP, LARGE_BUFF)
        number = equation[0]
        alt_rhs_list = list(it.starmap(Tex, [
            ("\\ne", "2^2 \\cdot 563"),
            ("\\ne", "2^2 \\cdot 3 \\cdot 11 \\cdot 17"),
            ("\\ne", "2 \\cdot 7^2 \\cdot 23"),
            ("=", "(-2) \\cdot (-3) \\cdot (3) \\cdot 5^3"),
            ("=", "2 \\cdot (-3) \\cdot (3) \\cdot (-5) \\cdot 5^2"),
        ]))
        for alt_rhs in alt_rhs_list:
            if "\\ne" in alt_rhs.get_tex():
                alt_rhs.set_color(RED)
            else:
                alt_rhs.set_color(GREEN)
            alt_rhs.move_to(equation.get_right())
        number.save_state()
        number.next_to(self.teacher, UP+LEFT)
        title = OldTexText("Almost", "Unique factorization")
        title.set_color_by_tex("Almost", YELLOW)
        title.to_edge(UP)

        self.play(
            self.teacher.change_mode, "raise_right_hand",
            Write(number)
        )
        self.wait(2)
        self.play(
            number.restore,
            Write(VGroup(*equation[1:])),
            Write(title[1])
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = equation,
            added_anims = [self.teacher.change_mode, "happy"]
        )
        self.wait()
        last_alt_rhs = None
        for alt_rhs in alt_rhs_list:
            equation.generate_target()
            equation.target.next_to(alt_rhs, LEFT)
            anims = [MoveToTarget(equation)]
            if last_alt_rhs:
                anims += [ReplacementTransform(last_alt_rhs, alt_rhs)]
            else:
                anims += [FadeIn(alt_rhs)]
            self.play(*anims)
            if alt_rhs is alt_rhs_list[-2]:
                self.play_student_changes(
                    *["sassy"]*3,
                    look_at = alt_rhs,
                    added_anims = [Write(title[0])]
                )
            self.wait(2)
            last_alt_rhs = alt_rhs

        self.play(
            FadeOut(VGroup(equation, alt_rhs)),
            PiCreatureSays(
                self.teacher,
                "It's similar for \\\\ Gaussian integers",
                bubble_config = {"height" : 3.5}
            )
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(3)
