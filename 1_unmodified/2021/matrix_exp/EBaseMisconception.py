# ==============================================================================
# Scene:      EBaseMisconception
# Source:     videos/_2021/matrix_exp.py (lines 3301-3326)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EBaseMisconception.py EBaseMisconception -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EBaseMisconception(Scene):
    def construct(self):
        randy = Randolph()
        randy.flip()
        randy.to_corner(DR)
        self.add(randy)
        self.play(
            PiCreatureSays(
                randy, OldTexText("This function is\\\\about about $e$", tex_to_color_map={"$e$": BLUE}),
                target_mode="thinking",
                bubble_config={"height": 3, "width": 4},
            )
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("tease"))
        self.play(Blink(randy))
        cross = Cross(randy.bubble.content, stroke_width=[0, 5, 5, 5, 0])
        for line in cross:
            line.insert_n_curves(10)
        cross.scale(1.25)
        self.play(
            ShowCreation(cross),
            randy.change("guilty")
        )
        self.wait()
