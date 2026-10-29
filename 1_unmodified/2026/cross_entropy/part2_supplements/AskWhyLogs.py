# ==============================================================================
# Scene:      AskWhyLogs
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 65-76)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyLogs.py AskWhyLogs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhyLogs(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.flip()
        randy.to_edge(RIGHT)

        self.play(randy.says("Why logs?", mode="maybe", look_at=ORIGIN))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("confused"))
        self.wait()
