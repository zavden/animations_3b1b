# ==============================================================================
# Scene:      ShowCubeDVIn3D
# Source:     videos/_2017/eoc/chapter3.py (lines 1193-1195)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ShowCubeDVIn3D.py ShowCubeDVIn3D -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - none: category 3 (stage_scenes marker, same in Cairo)
#
# Why it does not render:
#   Marker scene: construct() raises "This scene is only here for the stage_scenes script." on purpose (it only registers the name for Grant's staging script and has no animation), same in Cairo.
# ==============================================================================

from manim_imports_ext import *

class ShowCubeDVIn3D(Scene):
    def construct(self):
        raise Exception("This scene is only here for the stage_scenes script.")
