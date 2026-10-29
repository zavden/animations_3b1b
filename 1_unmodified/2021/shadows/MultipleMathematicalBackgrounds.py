# ==============================================================================
# Scene:      MultipleMathematicalBackgrounds
# Source:     videos/_2021/shadows.py (lines 5978-6046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultipleMathematicalBackgrounds.py MultipleMathematicalBackgrounds -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MultipleMathematicalBackgrounds(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        labels = VGroup(
            OldTexText("$\\le$ High school"),
            OldTexText("$\\approx$ Undergrad"),
            OldTexText("$\\ge$ Ph.D."),
        )
        for student, label in zip(self.students, labels):
            label.scale(0.7)
            label.next_to(student, UP)

        words = OldTexText("Explanation doesn't vary\\\\with backgrounds")
        words.to_edge(UP)

        lines = VGroup(*(
            DashedLine(words, label, buff=0.5)
            for label in labels
        ))
        lines.set_stroke(WHITE, 2)

        self.add(words)
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students(
                "pondering", "thinking", "pondering",
                look_at=self.teacher.eyes,
            ),
        )
        self.play(
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.5),
            LaggedStartMap(FadeIn, labels, lag_ratio=0.5),
        )
        self.wait(3)
        self.play(
            self.teacher.change("dejected").look(UP),
            self.change_students("hesitant", "well", "thinking"),
            LaggedStartMap(FadeOut, lines, scale=0.5),
            FadeOut(words, DOWN),
        )
        self.wait(4)

        # Different levels
        kw = {"font_size": 30}
        methods = VGroup(
            OldTexText("Calculus\\\\primer", **kw),
            OldTexText("Quickly show\\\\key steps", **kw),
            OldTexText("Describe as a\\\\measure on SO(3)", **kw),
        )
        new_lines = VGroup()
        colors = [GREEN_B, GREEN_C, GREEN_D]
        for method, label, color in zip(methods, labels, colors):
            method.move_to(label)
            method.shift(2.5 * UP)
            method.set_color(color)
            line = DashedLine(method, label, buff=0.25)
            line.set_stroke(color, 2)
            new_lines.add(line)

        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students(
                "erm", "pondering", "thinking",
                look_at=self.students.get_center() + 4 * UP
            ),
            LaggedStartMap(FadeIn, methods, lag_ratio=0.5),
            LaggedStartMap(ShowCreation, new_lines, lag_ratio=0.5),
        )
        self.wait(4)
