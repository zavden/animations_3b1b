# ==============================================================================
# Scene:      DiscussTrilogy
# Source:     videos/_2025/laplace/supplements.py (lines 150-179)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiscussTrilogy.py DiscussTrilogy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DiscussTrilogy(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        screens = ScreenRectangle().replicate(3)
        screens.set_width(0.3 * FRAME_WIDTH)
        screens.arrange(RIGHT, buff=0.25 * (FRAME_WIDTH - 3 * screens[0].get_width()))
        screens.set_width(FRAME_WIDTH - 1)
        screens.to_edge(UP)

        # Reference last two
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(200)
        morty = self.teacher
        morty.change_mode("tease")
        brace1 = Brace(screens[0], DOWN)
        brace2 = Brace(screens[1:3], DOWN)

        self.wait(2)
        self.play(
            morty.change("raise_left_hand", look_at=brace2),
            self.change_students("pondering", "erm", "sassy", look_at=brace2),
            GrowFromCenter(brace2),
        )
        self.wait(3)
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("thinking", "pondering", "pondering", look_at=brace1),
            ReplacementTransform(brace2, brace1, path_arc=-30 * DEG),
        )
        self.wait(6)
