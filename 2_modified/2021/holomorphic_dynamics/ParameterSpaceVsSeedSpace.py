# ==============================================================================
# Scene:      ParameterSpaceVsSeedSpace
# Source:     videos/_2021/holomorphic_dynamics.py (lines 917-954)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ParameterSpaceVsSeedSpace.py ParameterSpaceVsSeedSpace -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex no longer accepts OldTex: it has no get_symbol_substrings)
# ==============================================================================

from manim_imports_ext import *

class ParameterSpaceVsSeedSpace(Scene):
    def construct(self):
        boxes = Square().get_grid(2, 2, buff=0)
        boxes.set_stroke(WHITE, 2)
        boxes.set_height(6)
        boxes.set_width(10, stretch=True)
        boxes.to_corner(DR)
        self.add(boxes)

        f_labels = VGroup(
            OldTex("f(z) = z^2 + c"),
            OldTex("f(z) = z - {P(z) \\over P'(z)}"),
        )
        kw = {
            "tex_to_color_map": {
                "function": YELLOW,
                "seed": BLUE_D,
            }
        }
        top_labels = VGroup(
            OldTexText("One seed\\\\Pixel $\\leftrightarrow$ function", **kw),
            OldTexText("One function\\\\Pixel $\\leftrightarrow$ seed", **kw),
        )
        for f_label, box in zip(f_labels, boxes[::2]):
            f_label.set_max_width(3.25)
            f_label.next_to(box, LEFT)
        for top_label, box in zip(top_labels, boxes):
            top_label.next_to(box, UP, buff=0.2)

        for f_label in f_labels:
            self.play(FadeIn(f_label, 0.25 * LEFT))
        self.wait()
        self.play(FadeIn(top_labels[0]))
        self.wait()
        # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
        self.play(TransformMatchingShapes(
            top_labels[0].copy(), top_labels[1]
        ))
        self.wait()
