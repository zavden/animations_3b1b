# ==============================================================================
# Scene:      SphereProjectionsWrapper
# Source:     videos/_2018/quaternions.py (lines 4638-4677)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereProjectionsWrapper.py SphereProjectionsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereProjectionsWrapper(Scene):
    def construct(self):
        rect_rows = VGroup(*[
            VGroup(*[
                ScreenRectangle(height=3)
                for x in range(3)
            ]).arrange(RIGHT, buff=LARGE_BUFF)
            for y in range(2)
        ]).arrange(DOWN, buff=2 * LARGE_BUFF)
        rect_rows.set_width(FRAME_WIDTH - 1)

        sphere_labels = VGroup(
            OldTexText("Circle in 2d"),
            OldTexText("Sphere in 3d"),
            OldTexText("Hypersphere in 4d"),
        )
        for label, rect in zip(sphere_labels, rect_rows[0]):
            label.next_to(rect, UP)

        projected_labels = VGroup(
            OldTexText("Sterographically projected \\\\ circle in 1d"),
            OldTexText("Sterographically projected \\\\ sphere in 2d"),
            OldTexText("Sterographically projected \\\\ hypersphere in 3d"),
        )
        for label, rect in zip(projected_labels, rect_rows[1]):
            label.match_width(rect)
            label.next_to(rect, UP)

        q_marks = OldTex("???")
        q_marks.scale(2)
        q_marks.move_to(rect_rows[0][2])

        self.add(rect_rows)
        for l1, l2 in zip(sphere_labels, projected_labels):
            added_anims = []
            if l1 is sphere_labels[2]:
                added_anims.append(FadeIn(q_marks))
            self.play(FadeIn(l1), *added_anims)
            self.play(FadeIn(l2))
            self.wait()
