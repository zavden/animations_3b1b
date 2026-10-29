# ==============================================================================
# Scene:      ThinkAboutWhatPropertyMeans
# Source:     videos/_2021/newton_fractal.py (lines 4289-4308)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThinkAboutWhatPropertyMeans.py ThinkAboutWhatPropertyMeans -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/NewtonBoundaryProperty.png (cubic Newton fractal computed with numpy; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class ThinkAboutWhatPropertyMeans(TeacherStudentsScene):
    def construct(self):
        self.screen.set_height(4, about_edge=UL)
        self.add(self.screen)
        image = ImageMobject("NewtonBoundaryProperty")
        image.replace(self.screen)
        self.add(image)

        self.teacher_says(
            OldTexText("Think about what\\\\this tells us."),
            bubble_config={
                "height": 3,
                "width": 4,
            }
        )
        self.play_student_changes(
            "pondering", "thinking", "pondering",
            look_at=self.screen
        )
        self.wait(4)
