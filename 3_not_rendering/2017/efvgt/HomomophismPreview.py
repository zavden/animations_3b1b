# ==============================================================================
# Scene:      HomomophismPreview
# Source:     videos/_2017/efvgt.py (lines 188-190)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl HomomophismPreview.py HomomophismPreview -w -m --fps 15
#
# Why it does not render:
#   Placeholder scene: its construct() raises "Meant as a place holder, not to be excecuted" on purpose (the clip was made elsewhere), so there is nothing to render without inventing content.
# ==============================================================================

from manim_imports_ext import *

class HomomophismPreview(Scene):
    def construct(self):
        raise Exception("Meant as a place holder, not to be excecuted")
