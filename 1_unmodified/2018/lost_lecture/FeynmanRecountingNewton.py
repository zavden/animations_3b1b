# ==============================================================================
# Scene:      FeynmanRecountingNewton
# Source:     videos/_2018/lost_lecture.py (lines 2746-2780)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeynmanRecountingNewton.py FeynmanRecountingNewton -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeynmanRecountingNewton(Scene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
    }

    def construct(self):
        feynman_teaching = ImageMobject("Feynman_teaching")
        feynman_teaching.set_width(FRAME_WIDTH)

        newton = ImageMobject("Newton")
        principia = ImageMobject("Principia_equal_area")
        images = [newton, principia]
        for image in images:
            image.set_height(5)
        newton.to_corner(UL)
        principia.next_to(newton, RIGHT)
        for image in images:
            image.rect = SurroundingRectangle(
                image, color=WHITE, buff=0,
            )

        self.play(FadeInFromDown(feynman_teaching, run_time=2))
        self.wait()
        self.play(
            FadeInFromDown(newton),
            FadeInFromDown(newton.rect),
        )
        self.wait()
        self.play(*[
            FadeIn(
                mob, direction=3 * LEFT
            )
            for mob in (principia, principia.rect)
        ])
        self.wait()
