# ==============================================================================
# Scene:      MakingFilesABitSmaller
# Source:     videos/_2026/cross_entropy/language_tree_visualization/language_tree.py (lines 1000-1008)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MakingFilesABitSmaller.py MakingFilesABitSmaller -w -m --fps 15
#
# Notes:
#   ../images/file_icon.svg is the faithful conversion of images/file_icon.ai (PDF) to SVG with pdftocairo.
# ==============================================================================

from manim_imports_ext import *

class FileIcon(SVGMobject):
    def __init__(self):
        super().__init__("../images/file_icon.svg")


class MakingFilesABitSmaller(InteractiveScene):
    def construct(self):
        # Draw an arrow to a file icon
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, thickness=7).set_color(YELLOW)
        file = FileIcon().set_width(3).set_x(0.5 * (arrow.get_right()[0] + FRAME_WIDTH * 0.5))
        self.play(AnimationGroup(GrowArrow(arrow), GrowFromCenter(file), lag_ratio=0.3))

        # Make the file smaller
        self.play(file.animate.scale(0.5), run_time=2)
