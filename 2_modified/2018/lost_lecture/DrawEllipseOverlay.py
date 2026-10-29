# ==============================================================================
# Scene:      DrawEllipseOverlay
# Source:     videos/_2018/lost_lecture.py (lines 1163-1182)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DrawEllipseOverlay.py DrawEllipseOverlay -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - removed the unused ImageMobject of HeldUpEllipse.jpg (get_image_output_directory does not exist in GL and the image is never added to the scene)
# ==============================================================================

from manim_imports_ext import *

class DrawEllipseOverlay(Scene):
    def construct(self):
        ellipse = Circle()
        ellipse.stretch_to_fit_width(7.0)
        ellipse.stretch_to_fit_height(3.8)
        ellipse.shift(1.05 * UP + 0.48 * LEFT)
        ellipse.set_stroke(RED, 8)

        # CHANGE: removed the unused ImageMobject of HeldUpEllipse.jpg (get_image_output_directory does not exist in GL and the image is never added to the scene)
        # (unused reference screenshot of the video frame removed: it is never added to the scene)

        # self.add(image)
        self.play(ShowCreation(ellipse))
        self.wait()
        self.play(FadeOut(ellipse))
