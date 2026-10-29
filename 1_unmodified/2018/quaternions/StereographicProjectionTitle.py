# ==============================================================================
# Scene:      StereographicProjectionTitle
# Source:     videos/_2018/quaternions.py (lines 2282-2298)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StereographicProjectionTitle.py StereographicProjectionTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StereographicProjectionTitle(Scene):
    def construct(self):
        title = OldTexText("Stereographic projection")
        final_title = title.copy()
        final_title.set_width(10)
        final_title.to_edge(UP)

        title.rotate(-90 * DEGREES)
        title.next_to(RIGHT, RIGHT, SMALL_BUFF)
        title.apply_complex_function(np.exp)
        title.rotate(90 * DEGREES)
        title.set_height(6)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(Transform(title, final_title, run_time=2))
        self.wait()
