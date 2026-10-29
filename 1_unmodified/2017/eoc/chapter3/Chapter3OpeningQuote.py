# ==============================================================================
# Scene:      Chapter3OpeningQuote
# Source:     videos/_2017/eoc/chapter3.py (lines 9-20)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter3OpeningQuote.py Chapter3OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter3OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "You know, for a mathematician, he did not have \\\\ enough",
            "imagination.", 
            "But he has become a poet and \\\\ now he is fine.",
        ],
        "highlighted_quote_terms" : {
            "imagination." : BLUE,
        },
        "author" : "David Hilbert"
    }
