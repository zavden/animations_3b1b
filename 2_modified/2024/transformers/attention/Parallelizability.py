# ==============================================================================
# Scene:      Parallelizability
# Source:     videos/_2024/transformers/attention.py (lines 4036-4093)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Parallelizability.py Parallelizability -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/gpu_large.svg  (_lib/assets/generated/2024/transformers/make_attention_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Parallelizability(InteractiveScene):
    def construct(self):
        # Set up curves
        n_instances = 20
        comp_syms = Tex(R"+\,\times").replicate(n_instances)
        comp_syms.arrange(DOWN)
        comp_syms.set_height(5.5)
        comp_syms.to_edge(DOWN)
        left_point = comp_syms.get_left() + 2 * LEFT
        right_point = comp_syms.get_right() + 2 * RIGHT
        curves = VGroup()
        for sym in comp_syms:
            curve = VMobject()
            curve.start_new_path(left_point)
            curve.add_cubic_bezier_curve_to(
                left_point + RIGHT,
                sym.get_left() + LEFT,
                sym.get_left()
            )
            curve.add_line_to(sym.get_right())
            curve.add_cubic_bezier_curve_to(
                sym.get_right() + RIGHT,
                right_point + LEFT,
                right_point,
            )
            curve.insert_n_curves(10)
            curves.add(curve)
        curves.set_stroke(width=(0, 2, 2, 2, 0))
        curves.set_submobject_colors_by_gradient(TEAL, BLUE)

        # Setup words
        in_word = Text("Input")
        out_word = Text("output")
        in_word.next_to(left_point, LEFT, SMALL_BUFF)
        out_word.next_to(right_point, RIGHT, SMALL_BUFF)
        self.add(comp_syms, in_word, out_word)

        # GPU symbol
        gpu = SVGMobject("gpu_large.svg")
        gpu.set_fill(GREY_B)
        gpu.set_width(1.5)
        gpu.next_to(comp_syms, UP)
        gpu_name = Text("GPU")
        gpu_name.next_to(gpu, UP)
        gpu_name.set_fill(GREY_B)
        self.add(gpu, gpu_name)

        # Animation
        for n in range(4):
            curves.shuffle()
            self.play(
                LaggedStartMap(
                    ShowPassingFlash, curves,
                    lag_ratio=5e-3,
                    time_width=1.5,
                    run_time=4
                )
            )
