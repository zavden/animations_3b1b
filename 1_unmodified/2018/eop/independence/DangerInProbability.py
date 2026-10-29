# ==============================================================================
# Scene:      DangerInProbability
# Source:     videos/_2018/eop/independence.py (lines 124-152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DangerInProbability.py DangerInProbability -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DangerInProbability(Scene):
    def construct(self):
        warning = self.get_warning_sign()
        probability = OldTexText("Probability")
        probability.scale(2)

        self.play(Write(warning, run_time = 1))
        self.play(
            warning.next_to, probability, UP, LARGE_BUFF,
            LaggedStartMap(FadeIn, probability)
        )
        self.wait()


    #####

    def get_warning_sign(self):
        triangle = RegularPolygon(n = 3, start_angle = np.pi/2)
        triangle.set_stroke(RED, 12)
        triangle.set_height(2)
        bang = OldTexText("!")
        bang.set_height(0.6*triangle.get_height())
        bang.move_to(interpolate(
            triangle.get_bottom(),
            triangle.get_top(),
            0.4,
        ))
        triangle.add(bang)
        return triangle
