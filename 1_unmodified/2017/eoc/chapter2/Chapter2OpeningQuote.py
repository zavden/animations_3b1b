# ==============================================================================
# Scene:      Chapter2OpeningQuote
# Source:     videos/_2017/eoc/chapter2.py (lines 50-69)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter2OpeningQuote.py Chapter2OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter2OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "So far as the theories of mathematics are about",
            "reality,", 
            "they are not",
            "certain;", 
            "so far as they are",
            "certain,", 
            "they are not about",
            "reality.",
        ],
        "highlighted_quote_terms" : {
            "reality," : BLUE,
            "certain;" : GREEN,
            "certain," : GREEN,
            "reality." : BLUE,
        },
        "author" : "Albert Einstein"
    }
