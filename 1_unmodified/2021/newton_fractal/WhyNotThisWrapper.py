# ==============================================================================
# Scene:      WhyNotThisWrapper
# Source:     videos/_2021/newton_fractal.py (lines 3522-3529)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyNotThisWrapper.py WhyNotThisWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyNotThisWrapper(VideoWrapper):
    title = "Why not something like this?"
    animate_boundary = False
    title_config = {
        "font_size": 60,
        "color": RED,
    }
    wait_time = 2
