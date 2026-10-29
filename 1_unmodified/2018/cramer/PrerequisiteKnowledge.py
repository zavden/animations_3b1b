# ==============================================================================
# Scene:      PrerequisiteKnowledge
# Source:     videos/_2018/cramer.py (lines 261-299)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrerequisiteKnowledge.py PrerequisiteKnowledge -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PrerequisiteKnowledge(TeacherStudentsScene):
    CONFIG = {
        "camera_config": {"background_opacity": 1}
    }

    def construct(self):
        self.remove(*self.pi_creatures)
        randy = self.students[1]
        self.add(randy)

        title = OldTexText("Prerequisites")
        title.to_edge(UP)

        h_line = Line(LEFT, RIGHT).scale(5)
        h_line.next_to(title, DOWN)

        images = Group(*[
            ImageMobject("eola%d_thumbnail" % d)
            for d in [5, 7, 6]
        ])
        images.arrange(RIGHT, buff=LARGE_BUFF)
        images.next_to(h_line, DOWN, MED_LARGE_BUFF)
        for image in images:
            rect = SurroundingRectangle(image, color=BLUE)
            image.rect = rect

        self.add(title)
        self.play(
            ShowCreation(h_line),
            randy.change, "erm"
        )
        self.wait()
        for image in images:
            self.play(
                FadeInFromDown(image),
                FadeInFromDown(image.rect),
                randy.change, "pondering"
            )
            self.wait()
