# ==============================================================================
# Scene:      AnnotateDemo
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 5-54)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnnotateDemo.py AnnotateDemo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (DemoStill.jpg); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/DemoStill.jpg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AnnotateDemo(InteractiveScene):
    def construct(self):
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        image = ImageMobject("DemoStill")
        image.set_height(FRAME_HEIGHT)
        plane = NumberPlane().fade(0.25)
        # self.add(image)
        # self.add(plane)

        # Label sugar
        sugar_label = Text("Sugar solution\n(0.75g sucrose/mL water)")
        sugar_label.move_to(2.5 * UP)
        sugar_label.set_backstroke(BLACK, 3)
        arrow_kw = dict(stroke_color=RED, stroke_width=10)
        sugar_arrow = Arrow(sugar_label, plane.c2p(0, 0.5), **arrow_kw)

        self.play(
            Write(sugar_label, lag_ratio=0.01, run_time=2),
            ShowCreation(sugar_arrow),
        )
        self.wait()

        # Label light
        light_label = Text("White light\n(unpolarized)")
        light_label.match_y(sugar_label)
        light_label.match_style(sugar_label)
        light_label.to_edge(RIGHT)
        light_arrow = Arrow(light_label, plane.c2p(4.75, 0.85), buff=0.1, **arrow_kw)

        self.play(
            FadeTransform(sugar_label, light_label),
            ReplacementTransform(sugar_arrow, light_arrow),
        )
        self.wait()

        # Label polarizer
        filter_label = Text("Linearly polarizing filter\n(variable angle)")
        filter_label.set_x(3.5).to_edge(UP)
        filter_label.match_style(sugar_label)
        filter_arrow = Arrow(filter_label, plane.c2p(3.4, 1.25), buff=0.1, **arrow_kw)

        self.play(
            FadeTransform(light_label, filter_label),
            ReplacementTransform(light_arrow, filter_arrow),
        )
        self.wait()
        self.play(
            filter_label.animate.set_x(-2.2).to_edge(UP, buff=0.5),
            filter_arrow.animate.set_x(-3.3),
        )
        self.wait()
