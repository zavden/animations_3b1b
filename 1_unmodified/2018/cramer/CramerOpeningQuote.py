# ==============================================================================
# Scene:      CramerOpeningQuote
# Source:     videos/_2018/cramer.py (lines 114-118)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CramerOpeningQuote.py CramerOpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CramerOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote": ["Computers are useless. They \\\\ can only give you answers."],
        "author": "Pablo Picasso",
    }
