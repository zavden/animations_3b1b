# ==============================================================================
# Scene:      ShowSum
# Source:     videos/_2017/leibniz.py (lines 271-380)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSum.py ShowSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSum(TeacherStudentsScene):
    CONFIG = {
        "num_terms_to_add" : 40,
    }
    def construct(self):
        self.say_words()
        self.show_sum()

    def say_words(self):
        self.teacher_says("This won't be easy")
        self.play_student_changes(
            "hooray", "sassy", "angry"
        )
        self.wait(2)

    def show_sum(self):
        line = UnitInterval()
        line.add_numbers(0, 1)
        # line.shift(UP)
        sum_point = line.number_to_point(np.pi/4)

        numbers = [0] + [
            ((-1)**n)/(2.0*n + 1) 
            for n in range(self.num_terms_to_add)
        ]
        partial_sums = np.cumsum(numbers)
        points = list(map(line.number_to_point, partial_sums))
        arrows = [
            Arrow(
                p1, p2, 
                tip_length = 0.2*min(1, get_norm(p1-p2)),
                buff = 0
            )
            for p1, p2 in zip(points, points[1:])
        ]
        dot = Dot(points[0])

        sum_mob = OldTex(
            "1", "-\\frac{1}{3}", 
            "+\\frac{1}{5}", "-\\frac{1}{7}",
            "+\\frac{1}{9}", "-\\frac{1}{11}",
            "+\\cdots"
        )
        sum_mob.to_corner(UP+RIGHT)
        lhs = OldTex(
            "\\frac{\\pi}{4}", "=", 
        )
        lhs.next_to(sum_mob, LEFT)
        lhs.set_color_by_tex("pi", YELLOW)
        sum_arrow = Arrow(
            lhs.get_part_by_tex("pi").get_bottom(),
            sum_point
        )
        fading_terms = [
            OldTex(sign + "\\frac{1}{%d}"%(2*n + 1))
            for n, sign in zip(
                list(range(self.num_terms_to_add)),
                it.cycle("+-")
            )
        ]
        for fading_term, arrow in zip(fading_terms, arrows):
            fading_term.next_to(arrow, UP)

        terms = it.chain(sum_mob, it.repeat(None))
        last_arrows = it.chain([None], arrows)
        last_fading_terms = it.chain([None], fading_terms)

        self.play_student_changes(
            *["pondering"]*3,
            look_at = line,
            added_anims = [
                FadeIn(VGroup(line, dot)),
                FadeIn(lhs),
                RemovePiCreatureBubble(
                    self.teacher,
                    target_mode = "raise_right_hand"
                )
            ]
            
        )
        run_time = 1
        for term, arrow, last_arrow, fading_term, last_fading_term in zip(
            terms, arrows, last_arrows, fading_terms, last_fading_terms
            ):
            anims = []
            if term:
                anims.append(Write(term))
            if last_arrow:
                anims.append(FadeOut(last_arrow))
            if last_fading_term:
                anims.append(FadeOut(last_fading_term))
            dot_movement = ApplyMethod(dot.move_to, arrow.get_end())
            anims.append(ShowCreation(arrow))
            anims.append(dot_movement)
            anims.append(FadeIn(fading_term))
            self.play(*anims, run_time = run_time)
            if term:
                self.wait()
            else:
                run_time *= 0.8
        self.play(
            FadeOut(arrow),
            FadeOut(fading_term),
            dot.move_to, sum_point
        )
        self.play(ShowCreation(sum_arrow))
        self.wait()
        self.play_student_changes("erm", "confused", "maybe")
        self.play(self.teacher.change_mode, "happy")
        self.wait(2)
