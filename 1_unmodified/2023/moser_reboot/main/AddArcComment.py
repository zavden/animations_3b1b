# ==============================================================================
# Scene:      AddArcComment
# Source:     videos/_2023/moser_reboot/main.py (lines 1035-1040)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddArcComment.py AddArcComment -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AddArcComment(InteractiveScene):
    def construct(self):
        comment = TexText("$+n$ circular arcs")
        comment.to_corner(UL)
        comment.set_color(YELLOW)
        self.add(comment)
