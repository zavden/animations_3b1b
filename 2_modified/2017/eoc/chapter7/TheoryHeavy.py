# ==============================================================================
# Scene:      TheoryHeavy
# Source:     videos/_2017/eoc/chapter7.py (lines 1714-1799)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TheoryHeavy.py TheoryHeavy -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - student_says() default speaker is students[2] (sep19 and GL), not students[1]: FadeOut(None) failed
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class TheoryHeavy(TeacherStudentsScene):
    def construct(self):
        lhs = OldTex(
            "{df", "\\over \\,", "dx}", "(", "x", ")"
        )
        equals = OldTex("=")
        rhs = OldTex(
            "\\lim", "_{h", "\\to 0}", 
            "{f", "(", "x", "+", "h", ")", "-", "f", "(", "x", ")",
            "\\over \\,", "h}"
        )
        derivative = VGroup(lhs, equals, rhs)
        derivative.arrange(RIGHT)
        for tex_mob in derivative:
            tex_mob.set_color_by_tex("x", RED)
            tex_mob.set_color_by_tex("h", GREEN)
            tex_mob.set_color_by_tex("dx", GREEN)
            tex_mob.set_color_by_tex("f", YELLOW)
        derivative.next_to(self.get_pi_creatures(), UP, buff = MED_LARGE_BUFF)

        lim = rhs.get_part_by_tex("lim")
        epsilon_delta = OldTex("(\\epsilon, \\delta)")
        epsilon_delta.next_to(lim, UP, buff = 1.5*LARGE_BUFF)
        arrow = Arrow(epsilon_delta, lim, color = WHITE)


        self.student_says(
            "Too much theory!",
            target_mode = "angry",
            content_introduction_kwargs = {"run_time" : 2},
        )
        self.wait()
        # CHANGE: student_says() default speaker is students[2] (sep19 and GL), not students[1]: FadeOut(None) failed
        student = self.get_students()[2]
        Scene.play(self,
            Write(lhs),
            FadeOut(student.bubble),
            FadeOut(student.bubble.content),
            *[
                ApplyFunction(
                    lambda pi : pi.change_mode("pondering").look_at(epsilon_delta),
                    pi
                )
                for pi in self.get_pi_creatures()
            ]
        )
        student.bubble = None
        part_tex_pairs = [
            ("df", "f"),
            ("over", "+"),
            ("over", "-"),
            ("over", "to"),
            ("over", "over"),
            ("dx", "h"),
            ("(", "("),
            ("x", "x"),
            (")", ")"),
        ]
        self.play(Write(equals), Write(lim), *[
            ReplacementTransform(
                VGroup(*lhs.get_parts_by_tex(t1)).copy(),
                VGroup(*rhs.get_parts_by_tex(t2)),
                run_time = 2,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.5)
            )
            for (t1, t2), alpha in zip(
                part_tex_pairs,
                np.linspace(0, 0.5, len(part_tex_pairs))
            )
        ])
        self.wait(2)
        self.play(
            Write(epsilon_delta),
            ShowCreation(arrow)
        )
        self.wait(3)
        derivative.add(epsilon_delta, arrow)
        self.student_says(
            "How do you \\\\ compute limits?",
            index = 2,
            added_anims = [
                derivative.scale, 0.8,
                derivative.to_corner, UP+LEFT
            ]
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.wait(2)
