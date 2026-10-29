# ==============================================================================
# Scene:      Chapter9OpeningQuote
# Source:     videos/_2017/eoc/chapter9.py (lines 6-19)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter9OpeningQuote.py Chapter9OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter9OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "We often hear that mathematics consists mainly of", 
            "proving theorems.",
            "Is a writer's job mainly that of\\\\",
            "writing sentences?"
        ],
        "highlighted_quote_terms" : {
            "proving theorems." : MAROON_B,
            "writing sentences?" : MAROON_B,
        },
        "author" : "Gian-Carlo Rota",
    }
