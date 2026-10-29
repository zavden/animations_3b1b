# ==============================================================================
# Scene:      Chapter4OpeningQuote
# Source:     videos/_2017/eoc/chapter4.py (lines 8-16)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter4OpeningQuote.py Chapter4OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter4OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Using the chain rule is like peeling an onion: ",
            "you have to deal with each layer at a time, and ",
            "if it is too big you will start crying."
        ],
        "author" : "(Anonymous professor)"
    }
