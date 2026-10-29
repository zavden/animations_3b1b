# ==============================================================================
# Scene:      LostLecturePicture
# Source:     videos/_2018/lost_lecture.py (lines 1087-1102)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LostLecturePicture.py LostLecturePicture -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LostLecturePicture(TODOStub):
    CONFIG = {"camera_config": {"background_opacity": 1}}

    def construct(self):
        picture = ImageMobject("Feynman_teaching")
        picture.set_height(FRAME_WIDTH)
        picture.to_corner(UL, buff=0)
        picture.fade(0.5)

        self.play(
            picture.to_corner, DR, {"buff": 0},
            picture.shift, 1.5 * DOWN,
            path_arc=60 * DEGREES,
            run_time=20,
            rate_func=bezier([0, 0, 1, 1])
        )
