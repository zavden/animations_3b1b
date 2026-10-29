# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2017/eoc/chapter2.py (lines 71-161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Introduction(TeacherStudentsScene):
    def construct(self):
        goals = OldTexText(
            "Goals: ",
            "1) Learn derivatives", 
            ", 2) Avoid paradoxes.",
            arg_separator = ""
        )
        goals[1].set_color(MAROON_B)
        goals[2].set_color(RED)
        goals[2][0].set_color(WHITE)
        goals.to_edge(UP)
        self.add(*goals[:2])

        self.student_says(
            "What is a derivative?",
            run_time = 2
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.wait()
        self.teacher_says(
            "It's actually a \\\\",
            "very subtle idea",
            target_mode = "well"
        )
        self.play_student_changes(None, "pondering", "thinking")
        self.play(Write(goals[2], run_time = 2))
        self.play_student_changes("erm")
        self.student_says(
            "Instantaneous rate of change", "?",
            index = 0,
        )
        self.wait()

        bubble = self.get_students()[0].bubble
        phrase = bubble.content[0]
        bubble.content.remove(phrase)
        self.play(
            FadeOut(bubble),
            FadeOut(bubble.content),
            FadeOut(goals),
            phrase.center,
            phrase.scale, 1.5,
            phrase.to_edge, UP,
            *it.chain(*[
                [
                    pi.change_mode, mode,
                    pi.look_at, FRAME_Y_RADIUS*UP
                ]
                for pi, mode in zip(self.get_pi_creatures(), [
                    "speaking", "pondering", "confused", "confused",
                ])
            ])
        )
        self.wait()
        change = VGroup(*phrase[-len("change"):])
        instantaneous = VGroup(*phrase[:len("instantaneous")])
        change_brace = Brace(change)
        change_description = change_brace.get_text(
            "Requires multiple \\\\ points in time"
        )
        instantaneous_brace = Brace(instantaneous)
        instantaneous_description = instantaneous_brace.get_text(
            "One point \\\\ in time"
        )
        clock = Clock()
        clock.next_to(change_description, DOWN)
        def get_clock_anim(run_time = 3):
            return ClockPassesTime(
                clock,
                hours_passed = 0.4*run_time,
                run_time = run_time,
            )
        self.play(FadeIn(clock))
        self.play(
            change.set_color_by_gradient, BLUE, YELLOW,
            GrowFromCenter(change_brace),
            Write(change_description),
            get_clock_anim()
        )
        self.play(get_clock_anim(1))
        stopped_clock = clock.copy()
        stopped_clock.next_to(instantaneous_description, DOWN)
        self.play(
            instantaneous.set_color, BLUE,
            GrowFromCenter(instantaneous_brace),
            Transform(change_description.copy(), instantaneous_description),
            clock.copy().next_to, instantaneous_description, DOWN,
            get_clock_anim(3)
        )
        self.play(get_clock_anim(12))
