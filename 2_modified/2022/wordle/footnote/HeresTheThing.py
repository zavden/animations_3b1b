# ==============================================================================
# Scene:      HeresTheThing
# Source:     videos/_2022/wordle/footnote.py (lines 5-46)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HeresTheThing.py HeresTheThing -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The thumbnail is loaded with ImageMobject("WordleThumbnail") (placeholder) instead of the path <output folder>/2022/wordle/images/Thumbnail
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/WordleThumbnail.png (placeholder thumbnail; generator 2022/wordle/make_wordle_assets.py)
# ==============================================================================

from manim_imports_ext import *

class HeresTheThing(TeacherStudentsScene):
    def construct(self):
        # CHANGE: in the original the thumbnail lived in <output folder>/2022/wordle/images/Thumbnail; here it is a placeholder in _lib/assets/raster_images
        thumbnail = ImageMobject("WordleThumbnail")
        thumbnail = Group(
            SurroundingRectangle(thumbnail, buff=0, stroke_color=WHITE, stroke_width=2),
            thumbnail
        )
        thumbnail.set_height(3)
        thumbnail.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.teacher.change("raise_right_hand"),
            FadeIn(thumbnail, UP),
        )
        self.play_student_changes(
            "raise_left_hand", "pondering", "erm",
            look_at=self.teacher.eyes,
        )
        self.wait()
        self.teacher_says(
            OldTexText("Right, here's\\\\the thing...", font_size=40),
            target_mode="hesitant",
            bubble_config=dict(width=3.5, height=2.5),
            run_time=1,
            added_anims=[
                self.change_students("dance_3", "frustrated", "sassy"),
                thumbnail.animate.to_corner(UL),
            ]
        )
        self.look_at(thumbnail)
        cross = Cross(Text("CRANE"))
        cross.insert_n_curves(20)
        cross.move_to(thumbnail, UR)
        cross.shift([-0.25, -0.22, 0])
        self.play(ShowCreation(cross))
        self.wait(3)
