# ==============================================================================
# Scene:      AskAboutPhysicsRelation
# Source:     videos/_2022/wordle/scenes.py (lines 2295-2341)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutPhysicsRelation.py AskAboutPhysicsRelation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutPhysicsRelation(TeacherStudentsScene):
    def construct(self):
        physics = self.get_physics_entropy_image()
        physics.next_to(self.students[2], UL)
        physics.to_edge(UP)

        self.student_says(
            OldTexText("What does this have\\\\to do with thermodynamics?"),
            target_mode="raise_right_hand",
            index=2,
            bubble_config=dict(width=5, height=3, direction=LEFT),
        )
        self.play(self.teacher.change("tease"))
        self.play(
            self.students[0].change("pondering", physics),
            self.students[1].change("pondering", physics),
            self.students[2].change("raise_left_hand", physics),
            Write(physics),
        )
        self.wait(3)

        self.embed()

    def get_physics_entropy_image(self):
        dots = Dot().get_grid(14, 10)
        dots.set_height(3)
        n = len(dots)
        dots[:n // 2].set_color(RED)
        dots[n // 2:].set_color(BLUE)

        dots_copy = dots.deepcopy()
        dots_copy.set_color(RED)
        VGroup(*random.sample(list(dots_copy), n // 2)).set_color(BLUE)

        pair = VGroup(dots, dots_copy)
        pair.arrange(RIGHT, buff=LARGE_BUFF)
        rects = VGroup(*map(SurroundingRectangle, pair))
        rects.set_stroke(WHITE, 1)
        labels = VGroup(
            Text("Low entropy"),
            Text("High entropy"),
        )
        labels.scale(0.75)
        for label, rect in zip(labels, rects):
            label.next_to(rect, UP)

        return VGroup(labels, rects, pair)
