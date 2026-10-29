# ==============================================================================
# Scene:      ReferenceSmallAngleApproximations
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 715-758)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceSmallAngleApproximations.py ReferenceSmallAngleApproximations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceSmallAngleApproximations(TeacherStudentsScene):
    def construct(self):
        self.add_title()
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        # Test
        equation1 = Tex(R"\arctan(x) \approx x")
        equation1[R"\arctan"].set_color(GREEN)
        equation2 = Tex(R"x \approx \tan(x)")
        equation2[R"\tan"].set_color(YELLOW)
        for mob in equation1, equation2:
            mob.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeIn(equation1, UP),
            self.teacher.change("raise_right_hand"),
            self.change_students(
                "erm", "sassy", "confused"
            )
        )
        self.look_at(3 * UL)
        self.play(equation1.animate.shift(UP))
        self.play(
            TransformMatchingTex(
                equation1.copy(),
                equation2,
                lag_ratio=0.01,
                key_map={R"\arctan": R"\tan"}
            )
        )
        self.play(self.change_students("confused", "erm", "sassy"))
        self.look_at(3 * UL)
        self.wait(3)

    def add_title(self):
        title = TexText("For small $x$")
        subtitle = TexText("(e.g. $x = 0.001$)")
        subtitle.scale(0.75)
        subtitle.next_to(title, DOWN)
        title.add(subtitle)
        title.move_to(self.hold_up_spot)
        title.to_edge(UP)
        self.add(title)
