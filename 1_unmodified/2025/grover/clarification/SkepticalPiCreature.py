# ==============================================================================
# Scene:      SkepticalPiCreature
# Source:     videos/_2025/grover/clarification.py (lines 1403-1427)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SkepticalPiCreature.py SkepticalPiCreature -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SkepticalPiCreature(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph().to_edge(DOWN).shift(3 * LEFT)
        randy.body.set_color(MAROON_E)
        morty = Mortimer().to_edge(DOWN).shift(3 * RIGHT)
        morty.make_eye_contact(randy)
        for pi in [randy, morty]:
            pi.change_mode("tease")
            pi.body.insert_n_curves(100)

        self.play(LaggedStart(
            randy.says("Quantum Computing will\nchange everything!", mode="surprised"),
            morty.change("hesitant")
        ))
        self.play(Blink(morty))
        self.wait(2)
        self.play(Blink(randy))
        self.add(Point())
        self.play(
            morty.says("...will it?", mode="sassy"),
            randy.change("guilty"),
        )
        self.play(Blink(morty))
        self.wait()
