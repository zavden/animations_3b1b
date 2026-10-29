# ==============================================================================
# Scene:      ExpFootnoteOpeningQuote
# Source:     videos/_2017/eoc/chapter5.py (lines 4-15)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpFootnoteOpeningQuote.py ExpFootnoteOpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpFootnoteOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
        "Who has not been amazed to learn that the function",
        "$y = e^x$,", "like a phoenix rising again from its own",
        "ashes, is its own derivative?",
        ],
        "highlighted_quote_terms" : {
            "$y = e^x$" : MAROON_B
        },
        "author" : "Francois le Lionnais"
    }
