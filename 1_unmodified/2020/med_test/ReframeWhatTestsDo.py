# ==============================================================================
# Scene:      ReframeWhatTestsDo
# Source:     videos/_2020/med_test.py (lines 4324-4441)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReframeWhatTestsDo.py ReframeWhatTestsDo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReframeWhatTestsDo(TeacherStudentsScene):
    def construct(self):
        # Question
        question = OldTexText("What do tests tell you?")
        self.teacher_holds_up(question)
        self.wait()

        question.generate_target()
        question.target.set_height(0.6)
        question.target.center()
        question.target.to_edge(UP)
        self.play(
            MoveToTarget(question),
            *[
                ApplyMethod(pi.change, "pondering", question.target)
                for pi in self.pi_creatures
            ]
        )
        self.wait(2)

        # Possible answers
        answers = VGroup(
            OldTexText("Tests", " determine", " if you have", " a disease."),
            OldTexText("Tests", " determine", " your chances of having", " a disease."),
            OldTexText("Tests", " update", " your chances of having", " a disease."),
        )
        students = self.students
        answers.set_color(BLUE_C)
        answers.arrange(DOWN)
        answers.next_to(question, DOWN, MED_LARGE_BUFF)

        answers[1][2].set_fill(GREY_A)
        answers[2][2].set_fill(GREY_A)
        answers[2][1].set_fill(YELLOW)

        def add_strike_anim(words):
            strike = Line()
            strike.replace(words, dim_to_match=0)
            strike.set_stroke(RED, 5)
            anim = ShowCreation(strike)
            words.add(strike)
            return anim

        self.play(
            GrowFromPoint(answers[0], students[0].get_corner(UR)),
            students[0].change, "raise_right_hand", answers[0],
            students[1].change, "sassy", students[0].eyes,
            students[2].change, "sassy", students[0].eyes,
        )
        self.wait()
        self.play(
            add_strike_anim(answers[0]),
            students[0].change, "guilty",
        )
        self.wait()

        answers[1][2].save_state()
        answers[1][2].replace(answers[0][2], stretch=True)
        answers[1][2].set_opacity(0)
        self.play(
            TransformFromCopy(
                answers[0][:2],
                answers[1][:2],
            ),
            TransformFromCopy(
                answers[0][3],
                answers[1][3],
            ),
            Restore(answers[1][2]),
            students[0].set_opacity, 0.5,
            students[0].change, "pondering", answers[1],
            students[1].change, "raise_right_hand", answers[1],
            students[2].change, "pondering", answers[1],
        )
        self.wait(2)
        self.play(
            add_strike_anim(answers[1]),
            students[1].change, "guilty",
        )
        self.wait(2)

        answers[2][1].save_state()
        answers[2][1].replace(answers[1][1], stretch=True)
        answers[2][1].set_opacity(0)
        self.play(
            *(
                TransformFromCopy(
                    answers[1][i],
                    answers[2][i],
                )
                for i in [0, 2, 3]
            ),
            Restore(answers[2][1]),
            students[0].change, "pondering", answers[1],
            students[1].set_opacity, 0.5,
            students[1].change, "pondering", answers[1],
            students[2].change, "raise_left_hand", answers[1],
        )
        self.play(
            self.teacher.change, "happy", students[2].eyes,
        )
        self.wait()

        # The fundamental reframing
        new_title = OldTexText(
            "The Fundamental Reframing",
            font_size=72,
        )
        new_title.add(Underline(new_title))
        new_title.to_edge(UP)

        self.play(
            Write(new_title),
            FadeOut(question),
            self.students[2].change, "hooray", new_title,
            answers.shift, 0.5 * DOWN,
        )
        self.wait(3)
