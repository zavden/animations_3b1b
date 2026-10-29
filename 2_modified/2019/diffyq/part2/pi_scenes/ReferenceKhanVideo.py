# ==============================================================================
# Scene:      ReferenceKhanVideo
# Source:     videos/_2019/diffyq/part2/pi_scenes.py (lines 125-142)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReferenceKhanVideo.py ReferenceKhanVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ReferenceKhanVideo(TeacherStudentsScene):
    def construct(self):
        khan_logo = ImageMobject("KhanLogo")
        khan_logo.set_height(1)
        khan_logo.next_to(self.teacher, UP, buff=2)
        khan_logo.shift(2 * LEFT)

        self.play(
            self.teacher.change, "raise_right_hand",
        )
        self.play_student_changes(
            "thinking", "pondering", "thinking",
            look_at=self.screen
        )
        self.wait()
        self.play(FadeInFromDown(khan_logo))
        self.look_at(self.screen)
        self.wait(15)
