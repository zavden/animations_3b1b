# ==============================================================================
# Scene:      SubPiComment
# Source:     videos/_2022/borwein/supplements.py (lines 407-419)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SubPiComment.py SubPiComment -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Typo in the original: morty.animte -> morty.animate
# ==============================================================================

from manim_imports_ext import *

class SubPiComment(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=2).flip()
        morty.to_corner(DL)

        self.play(
            morty.says(OldTex(R"x \rightarrow \pi x", tex_to_color_map={R"\pi": TEAL}))
        )
        # CHANGE: typo in the original: "animte" instead of "animate"
        self.play(morty.animate.look(RIGHT))
        for x in range(2):
            self.play(Blink(morty))
            self.play(morty.animate.look(DR + x * DOWN))
            self.wait(2)
