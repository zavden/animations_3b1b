# ==============================================================================
# Scene:      LightBouncingOffFogParticle
# Source:     videos/_2018/turbulence.py (lines 533-545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightBouncingOffFogParticle.py LightBouncingOffFogParticle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LightBouncingOffFogParticle(Scene):
    def construct(self):
        words = OldTexText(
            "Light bouncing\\\\",
            "off fog particles"
        )
        arrow = Vector(UP + 0.5 * RIGHT)
        arrow.next_to(words, UP)
        arrow.set_color(WHITE)

        self.add(words)
        self.play(GrowArrow(arrow))
        self.wait()
