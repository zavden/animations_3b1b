# ==============================================================================
# Scene:      NumberphileFrame
# Source:     videos/_2021/shadows.py (lines 6569-6575)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NumberphileFrame.py NumberphileFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NumberphileFrame(VideoWrapper):
    animate_boundary = True
    title = "Bertrand's Paradox (with Numberphile)"
    title_config = {
        "font_size": 48
    }
    wait_time = 16
