# ==============================================================================
# Scene:      ReactingToCosineMachine
# Source:     videos/_2025/laplace/main_supplements.py (lines 652-672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactingToCosineMachine.py ReactingToCosineMachine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReactingToCosineMachine(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.flip()
        randy.to_edge(RIGHT)
        randy.shift(DOWN)

        for mode in ["erm", "confused"]:
            self.play(randy.change(mode))
            self.play(Blink(randy))
            self.wait(2)

        # Consider expression
        randy.body.insert_n_curves(500)
        self.play(randy.change("thinking", look_at=3 * UR))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("tease", look_at=randy.get_top() + 2 * UP))
        self.play(Blink(randy))
        self.wait(5)
