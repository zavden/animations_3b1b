# ==============================================================================
# Scene:      HeisenbergCommentTodos
# Source:     videos/_2018/uncertainty.py (lines 4126-4129)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/fourier.py
#
# Run from this folder:
#     manimgl HeisenbergCommentTodos.py HeisenbergCommentTodos -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/fourier.py -----

class TODOStub(Scene):
    def construct(self):
        pass



# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class HeisenbergCommentTodos(TODOStub):
    CONFIG = {
        "message" : "Insert position-momentum trade-off"
    }
