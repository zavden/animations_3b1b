# ==============================================================================
# Scene:      ManyExponentialForms
# Source:     videos/_2017/eoc/chapter5.py (lines 1582-1639)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyExponentialForms.py ManyExponentialForms -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyExponentialForms(TeacherStudentsScene):
    def construct(self):
        lhs = OldTex("2", "^t")
        rhs_list = [
            OldTex("=", "%s^"%tex, "{(%.5f\\dots)"%log, "t}")
            for tex, log in [
                ("e", np.log(2)),
                ("\\pi", np.log(2)/np.log(np.pi)),
                ("42", np.log(2)/np.log(42)),
            ]
        ]
        group = VGroup(lhs, *rhs_list)
        group.arrange(RIGHT)
        group.set_width(FRAME_WIDTH - LARGE_BUFF)
        group.next_to(self.get_pi_creatures(), UP, 2*LARGE_BUFF)
        for part in group:
            part.set_color_by_tex("t", YELLOW)
            const = part.get_part_by_tex("dots")
            if const:
                const.set_color(BLUE)
                brace = Brace(const, UP)
                log = brace.get_text(
                    "$\\log_{%s}(2)$"%part[1].get_tex()[:-1]
                )
                log.set_color(BLUE)
                part.add(brace, log)
        exp = VGroup(*rhs_list[0][1:4])
        rect = BackgroundRectangle(group)

        self.add(lhs, rhs_list[0])
        self.wait()
        for rhs in rhs_list[1:]:
            self.play(FadeIn(
                rhs, 
                run_time = 2,
                lag_ratio = 0.5,
            ))
            self.wait(2)
        self.wait()
        self.play(
            FadeIn(rect),
            exp.next_to, self.teacher, UP+LEFT,
            self.teacher.change, "raise_right_hand",
        )
        self.play(*[
            ApplyFunction(
                lambda m : m.shift(SMALL_BUFF*UP).set_color(RED),
                part,
                run_time = 2,
                rate_func = squish_rate_func(there_and_back, a, a+0.3)
            )
            for part, a in zip(exp[1], np.linspace(0, 0.7, len(exp[1])))
        ])
        self.play_student_changes(
            *["pondering"]*3,
            look_at = exp
        )
        self.wait(3)
