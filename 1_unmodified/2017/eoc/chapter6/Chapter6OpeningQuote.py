# ==============================================================================
# Scene:      Chapter6OpeningQuote
# Source:     videos/_2017/eoc/chapter6.py (lines 5-13)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter6OpeningQuote.py Chapter6OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter6OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Do not ask whether a ",
            "statement is true until",
            "you know what it means."
        ],
        "author" : "Errett Bishop"
    }
