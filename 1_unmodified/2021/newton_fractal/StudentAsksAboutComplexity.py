# ==============================================================================
# Scene:      StudentAsksAboutComplexity
# Source:     videos/_2021/newton_fractal.py (lines 3690-3754)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StudentAsksAboutComplexity.py StudentAsksAboutComplexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StudentAsksAboutComplexity(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Why is it\\\\so complicated?"),
            index=0,
            bubble_config={
                "height": 3,
                "width": 4,
            },
            added_anims=[
                self.students[1].change("confused", self.teacher.eyes),
                self.students[2].change("erm", self.teacher.eyes),
            ],
        )
        self.wait()
        self.play(
            self.teacher.change("shruggie"),
        )
        self.wait()
        self.play(LaggedStart(
            PiCreatureSays(
                self.teacher, OldTexText("Math is what\\\\it is"),
                target_mode="well",
                bubble_config={
                    "height": 3,
                    "width": 4,
                }
            ),
            self.students[1].change("maybe"),
            self.students[2].change("sassy"),
            lag_ratio=0.7,
        ))
        self.wait(2)

        why = self.students[0].bubble.content[0][:3]
        question = Text("Is this meaningful?")
        question.to_corner(UL)
        question.set_color(YELLOW)
        arrow = Arrow(question, why)
        arrow.set_stroke(YELLOW, 5)

        self.play(
            why.animate.set_color(YELLOW),
            Write(question),
            ShowCreation(arrow),
            LaggedStart(*(
                pi.change(mode, question)
                for pi, mode in zip(self.pi_creatures, ("well", "erm", "sassy", "hesitant"))
            ))
        )
        self.wait(2)

        cross = Cross(question)
        cross.set_stroke(RED, [1, *4 * [8], 1])
        words = Text("Surprisingly answerable!")
        words.next_to(question, RIGHT, LARGE_BUFF)
        new_arrow = Arrow(words[:10], why)
        new_arrow.set_stroke(WHITE, 5)
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="erm"),
            ShowCreation(cross),
            FadeIn(words),
            ShowCreation(new_arrow),
        )
        self.wait(2)
