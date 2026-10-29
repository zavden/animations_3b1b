# ==============================================================================
# Scene:      ClipsLogo
# Source:     videos/outside_videos/for_site.py (lines 221-229)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ClipsLogo.py ClipsLogo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument; add_pupil is redefined without sheen
# ==============================================================================

from manim_imports_ext import *

# CHANGE: Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument; add_pupil is redefined without sheen
class Logo(Logo):
    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)


class ClipsLogo(Scene):
    def construct(self):
        logo = Logo()
        logo.set_height(FRAME_HEIGHT - 0.5)
        square = Square(stroke_width=0, fill_color=BLACK, fill_opacity=1)
        square.scale(5)
        square.rotate(45 * DEGREES)
        square.move_to(ORIGIN, LEFT)
        self.add(logo, square)
