# ==============================================================================
# Scene:      ComplainAboutSimplisticModel
# Source:     videos/_2020/beta/beta3.py (lines 338-339)
# Category:   3 · Does not render
# Includes code copied from: _2020/beta/beta1.py
#
# Run from this folder:
#     manimgl ComplainAboutSimplisticModel.py ComplainAboutSimplisticModel -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class ComplainAboutSimplisticModel(ExternallyAnimatedScene): pass`, Grant's marker for a clip animated outside manim (screen capture or recording). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/beta1.py -----

class ComplainAboutSimplisticModel(TeacherStudentsScene):
    def construct(self):
        axes = self.get_experience_graph()

        self.add(axes)
        self.play(
            self.teacher.change, "raise_right_hand", axes,
            self.change_students(
                "pondering", "erm", "sassy",
                look_at=axes,
            ),
            ShowCreation(
                axes.graph,
                run_time=3,
                rate_func=linear,
            ),
        )
        self.wait(2)

        student = self.students[2]
        bubble = SpeechBubble(
            direction=LEFT,
            height=3,
            width=5,
        )
        bubble.pin_to(student)
        bubble.write("What about something\\\\like this?")

        self.play(
            axes.next_to, student, UL,
            VFadeOut(axes.graph),
            FadeIn(bubble),
            Write(bubble.content, run_time=1),
            student.change, "raise_left_hand",
            self.students[0].change, "thinking", axes,
            self.students[1].change, "thinking", axes,
            self.teacher.change, "happy",
        )

        new_graph = VMobject()
        new_graph.set_points_as_corners([
            axes.c2p(0, 0.75),
            axes.c2p(2, 0.9),
            axes.c2p(4, 0.5),
            axes.c2p(6, 0.75),
            axes.c2p(8, 0.55),
            axes.c2p(10, 0.95),
        ])
        new_graph.make_smooth()
        new_graph.set_stroke([YELLOW, RED, GREEN], 2)

        self.play(
            ShowCreation(new_graph),
            *[
                ApplyMethod(pi.look_at, new_graph)
                for pi in self.pi_creatures
            ]
        )
        self.wait(3)

    def get_experience_graph(self):
        axes = Axes(
            x_min=-1,
            x_max=10,
            y_min=0,
            y_max=1.25,
            y_axis_config={
                "unit_size": 5,
                "tick_frequency": 0.25,
                "include_tip": False,
            }
        )
        axes.set_stroke(GREY_B, 1)
        axes.set_height(3)
        y_label = OldTexText("Experience quality")
        y_label.scale(0.5)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, SMALL_BUFF)
        axes.add(y_label)

        lines = VGroup()
        for x in range(10):
            lines.add(
                Line(axes.c2p(x, 0), axes.c2p(x + 0.9, 0))
            )
        lines.set_stroke(RED, 3)
        for line in lines:
            if random.random() < 0.5:
                line.set_y(axes.c2p(0, 1)[1])
                line.set_stroke(GREEN)

        axes.add(lines)
        axes.graph = lines

        rect = BackgroundRectangle(axes, buff=0.25)
        rect.set_stroke(WHITE, 1)
        rect.set_fill(BLACK, 1)

        axes.add_to_back(rect)
        axes.to_corner(UR)

        return axes



# ----- From _2020/beta/beta3.py -----

class ComplainAboutSimplisticModel(ExternallyAnimatedScene):
    pass
