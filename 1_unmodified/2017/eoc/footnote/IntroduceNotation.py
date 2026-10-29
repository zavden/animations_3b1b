# ==============================================================================
# Scene:      IntroduceNotation
# Source:     videos/_2017/eoc/footnote.py (lines 303-397)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceNotation.py IntroduceNotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceNotation(TeacherStudentsScene):
    def construct(self):
        clunky_deriv = OldTex(
            "{d", "\\big(", "{df", "\\over", "dx}", "\\big)",
            "\\over", "dx }"
        )
        over_index = clunky_deriv.index_of_part(
            clunky_deriv.get_parts_by_tex("\\over")[1]
        )
        numerator = VGroup(*clunky_deriv[:over_index])
        denominator = VGroup(*clunky_deriv[over_index+1:])


        rp = clunky_deriv.get_part_by_tex("(")
        lp = clunky_deriv.get_part_by_tex(")")
        dfs, overs, dxs = list(map(clunky_deriv.get_parts_by_tex, [
            "df", "over", "dx"
        ]))
        df_over_dx = VGroup(dfs[0], overs[0], dxs[0])
        d = clunky_deriv.get_part_by_tex("d")
        d_over_dx = VGroup(d, overs[1], dxs[1])

        d2f_over_dx2 = OldTex("{d^2 f", "\\over", "dx", "^2}")
        d2f_over_dx2.set_color_by_tex("dx", YELLOW)

        for mob in clunky_deriv, d2f_over_dx2:
            mob.next_to(self.teacher, UP+LEFT)

        for mob in numerator, denominator:
            circle = Circle(color = YELLOW)
            circle.replace(mob, stretch = True)
            circle.scale(1.3)
            mob.circle = circle
        dx_to_zero = OldTex("dx \\to 0")
        dx_to_zero.set_color(YELLOW)
        dx_to_zero.next_to(clunky_deriv, UP+LEFT)

        self.student_says(
            "What's that notation?",
            target_mode = "raise_left_hand"
        )
        self.play_student_changes("confused", "raise_left_hand", "confused")
        self.play(
            FadeIn(
                clunky_deriv,
                run_time = 2,
                lag_ratio = 0.5
            ),
            RemovePiCreatureBubble(self.get_students()[1]),
            self.teacher.change_mode, "raise_right_hand"
        )
        self.wait()
        self.play(ShowCreation(numerator.circle))
        self.wait()
        self.play(ReplacementTransform(
            numerator.circle,
            denominator.circle,
        ))
        self.wait()
        self.play(
            FadeOut(denominator.circle),
            Write(dx_to_zero),
            dxs.set_color, YELLOW
        )
        self.wait()
        self.play(
            FadeOut(dx_to_zero),
            *[ApplyMethod(pi.change, "plain") for pi in self.get_pi_creatures()]
        )
        self.play(
            df_over_dx.scale, dxs[1].get_height()/dxs[0].get_height(),
            df_over_dx.move_to, d_over_dx, RIGHT,
            FadeOut(VGroup(lp, rp)),
            d_over_dx.shift, 0.8*LEFT + 0.05*UP,
        )
        self.wait()
        self.play(*[
            ReplacementTransform(
                group,
                VGroup(d2f_over_dx2.get_part_by_tex(tex))
            )
            for group, tex in [
                (VGroup(d, dfs[0]), "d^2"),
                (overs, "over"),
                (dxs, "dx"),
                (VGroup(dxs[1].copy()), "^2}"),
            ]
        ])
        self.wait(2)
        self.student_says(
            "How does one... \\\\ read that?",
            index = 0,
        )
        self.play(self.teacher.change, "happy")
        self.wait(2)
