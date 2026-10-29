# ==============================================================================
# Scene:      ReferenceGuessingExp
# Source:     videos/_2025/laplace/prequel_equations.py (lines 713-798)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceGuessingExp.py ReferenceGuessingExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceGuessingExp(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        # Student asks
        question = Tex(R"x(t) = ???")
        lhs = question["x(t)"][0]
        rhs = question["= ???"][0]
        bubble = stds[2].get_bubble(question, bubble_type=SpeechBubble, direction=LEFT)
        lhs.save_state()
        lhs.scale(0.25).move_to([-6.24, 2.38, 0])

        self.play(
            morty.change("hesitant", look_at=stds[2].eyes),
            self.change_students("erm", "confused", "maybe", look_at=self.screen)
        )
        self.wait()
        self.play(
            stds[2].change("raise_left_hand", morty.eyes),
            Write(bubble[0]),
            Write(rhs, time_span=(0.5, 1.0)),
            Restore(lhs),
        )
        self.wait()
        self.add(Point())
        self.play(
            morty.says("Here's a trick:", mode="tease", bubble_creation_class=FadeIn),
            self.change_students("pondering", "thinking", "hesitant", look_at=UL),
        )
        self.wait(2)

        # Teacher gestures to upper right, students look confused and hesitant
        eq_point = 5 * RIGHT + 3 * UP
        self.play(
            morty.change("raise_right_hand", look_at=eq_point),
            FadeOut(bubble),
            FadeOut(morty.bubble),
            self.change_students("confused", "thinking", "hesitant", look_at=eq_point),
        )
        self.wait()
        self.play(self.change_students("confused", "hesitant", "confused", look_at=eq_point, lag_ratio=0.1))
        self.wait()
        self.play(
            morty.change("shruggie", look_at=eq_point),
        )
        self.wait(2)
        self.play(
            self.change_students("angry", "hesitant", "erm", look_at=morty.eyes),
            morty.animate.look_at(stds)
        )
        self.wait(2)

        # Transition: flip and reposition morty to where stds are
        new_teacher_pos = stds[2].get_bottom()
        new_teacher = morty.copy()
        new_teacher.change_mode("raise_left_hand")
        new_teacher.look_at(3 * UR)
        new_teacher.body.set_color(GREY_C)

        self.play(
            morty.animate.scale(0.8).flip().change_mode("confused").look_at(5 * UR).move_to(new_teacher_pos, DOWN),
            LaggedStartMap(FadeOut, stds, shift=DOWN, lag_ratio=0.2, run_time=1),
            FadeIn(new_teacher, time_span=(0.5, 1.5)),
        )
        self.play(morty.change("pleading", 3 * UR))
        self.play(Blink(new_teacher))
        self.wait(2)
        self.play(LaggedStart(
            morty.change("erm", new_teacher.eyes),
            new_teacher.change("guilty", look_at=morty.eyes),
            lag_ratio=0.5,
        ))
        self.wait(3)

        # Reference a graph
        self.play(
            morty.change("angry", 2 * UR),
            new_teacher.change("tease", 2 * UR)
        )
        self.play(Blink(morty))
        self.play(Blink(new_teacher))
        self.wait()
