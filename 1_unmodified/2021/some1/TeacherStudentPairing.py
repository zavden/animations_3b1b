# ==============================================================================
# Scene:      TeacherStudentPairing
# Source:     videos/_2021/some1.py (lines 258-291)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TeacherStudentPairing.py TeacherStudentPairing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TeacherStudentPairing(Scene):
    def construct(self):
        randy = Randolph(height=2.5)
        morty = Mortimer(height=3.0)
        pis = VGroup(randy, morty)
        pis.arrange(RIGHT, buff=3, aligned_edge=DOWN)
        pis.to_edge(DOWN, buff=1.5)

        self.add(pis)
        self.add(Text("Teacher").next_to(morty, DOWN))
        self.add(Text("Student").next_to(randy, DOWN))

        teacher_label = Text("Delivers/writes lesson", font_size=36)
        student_label = Text("Produces/edits/animates", font_size=36)
        teacher_label.next_to(morty, UP, buff=1.5).shift(RIGHT)
        student_label.next_to(randy, UP, buff=1.5).shift(LEFT)
        teacher_arrow = Arrow(teacher_label, morty)
        student_arrow = Arrow(student_label, randy)

        self.play(
            Write(student_label),
            GrowArrow(student_arrow),
            randy.change("hooray", student_label)
        )
        self.wait()
        self.play(
            Write(teacher_label),
            GrowArrow(teacher_arrow),
            morty.change("pondering", teacher_label)
        )
        self.wait()
        for x in range(4):
            self.play(Blink(random.choice(pis)))
            self.wait(random.random())
