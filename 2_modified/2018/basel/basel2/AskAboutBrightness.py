# ==============================================================================
# Scene:      AskAboutBrightness
# Source:     videos/_2018/basel/basel2.py (lines 1162-1185)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskAboutBrightness.py AskAboutBrightness -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
# ==============================================================================

# CHANGE: import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint, scale, cutoff: inverse_power_law(maxint,scale,cutoff,2)


class AskAboutBrightness(TeacherStudentsScene):
    CONFIG = {
        "num_levels" : 200,
        "radius" : 10,
    }
    def construct(self):
        light_source = LightSource(
            num_levels = self.num_levels,
            radius = self.radius,
            opacity_function = inverse_quadratic(1,2,1),
        )
        light_source.lighthouse.scale(0.5, about_edge = UP)
        light_source.move_source_to(5*LEFT + 2*UP)

        self.add_foreground_mobjects(self.pi_creatures)
        self.student_says(
            "What do you mean \\\\ by ``brightness''?",
            added_anims = [
                SwitchOn(light_source.ambient_light),
                Animation(light_source.lighthouse)
            ]
        )
        self.play(self.teacher.change, "happy")
        self.wait(4)
