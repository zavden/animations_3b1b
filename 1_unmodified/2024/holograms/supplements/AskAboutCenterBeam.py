# ==============================================================================
# Scene:      AskAboutCenterBeam
# Source:     videos/_2024/holograms/supplements.py (lines 744-754)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutCenterBeam.py AskAboutCenterBeam -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutCenterBeam(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_edge(DOWN)
        self.play(
            randy.thinks("Why is there a\ncentral beam?", mode="confused")
        )
        self.play(Blink(randy))
        self.play(randy.animate.look_at(3 * UR))
        self.play(randy.animate.look_at(3 * DR))
