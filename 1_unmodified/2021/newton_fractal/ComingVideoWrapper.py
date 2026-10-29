# ==============================================================================
# Scene:      ComingVideoWrapper
# Source:     videos/_2021/newton_fractal.py (lines 1393-1395)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingVideoWrapper.py ComingVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingVideoWrapper(VideoWrapper):
    animate_boundary = False
    title = "Unsolvability of the Quintic (future topic?)"
