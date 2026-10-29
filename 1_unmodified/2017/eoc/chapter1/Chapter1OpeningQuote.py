# ==============================================================================
# Scene:      Chapter1OpeningQuote
# Source:     videos/_2017/eoc/chapter1.py (lines 256-269)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter1OpeningQuote.py Chapter1OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter1OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            """The art of doing mathematics is finding
            that """, "special case", 
            """that contains all the 
            germs of generality."""
        ],
        "quote_arg_separator" : " ",
        "highlighted_quote_terms" : {
            "special case" : BLUE
        },
        "author" : "David Hilbert",
    }
