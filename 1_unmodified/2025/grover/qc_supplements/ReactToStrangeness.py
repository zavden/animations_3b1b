# ==============================================================================
# Scene:      ReactToStrangeness
# Source:     videos/_2025/grover/qc_supplements.py (lines 360-372)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToStrangeness.py ReactToStrangeness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReactToStrangeness(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.flip()
        randy.to_corner(UR)

        self.play(randy.change('confused', ORIGIN))
        self.play(Blink(randy))
        self.play(randy.change('erm', ORIGIN))
        for _ in range(2):
            self.play(Blink(randy))
            self.wait(2)
